%lang starknet

from starkware.cairo.common.bool import TRUE, FALSE
from starkware.cairo.common.registers import get_fp_and_pc
from starkware.cairo.common.signature import verify_ecdsa_signature
from starkware.cairo.common.cairo_builtins import HashBuiltin, SignatureBuiltin
from starkware.cairo.common.alloc import alloc
from starkware.cairo.common.memcpy import memcpy
from starkware.cairo.common.math import assert_not_zero, assert_nn, assert_le
from starkware.cairo.common.math_cmp import is_le
from starkware.starknet.common.syscalls import (
  call_contract, get_caller_address, get_tx_info, get_contract_address, get_block_timestamp, library_call
)

//
// Libraries
//

from openzeppelin.utils.constants.library import IACCOUNT_ID, IERC165_ID

from periphery.utils.constants.library import IACCOUNT_ID_OLD
from periphery.proxy.library import Proxy

//
// Constants
//

const VERSION = '0.2.0';

const TRANSACTION_VERSION = 1;
const QUERY_VERSION = 2 ** 128 + TRANSACTION_VERSION;

//
// Structs
//

struct Call {
  to: felt,
  selector: felt,
  calldata_len: felt,
  calldata: felt*,
}

// Tmp struct introduced while we wait for Cairo
// to support passing `[AccountCall]` to __execute__
struct CallArray {
  to: felt,
  selector: felt,
  data_offset: felt,
  data_len: felt,
}

struct Escape {
  active_at: felt,
}

//
// Storage
//

@storage_var
func Account_signer_public_key() -> (res: felt) {
}

@storage_var
func Account_guardian_public_key() -> (res: felt) {
}

@storage_var
func Account_signer_escape() -> (res: Escape) {
}

//
// Events
//

@event
func AccountUpgraded(new_implementation: felt) {
}

@event
func AccountInitialized(signer_public_key: felt, guardian_public_key: felt) {
}

@event
func TransactionExecuted(hash: felt, response_len: felt, response: felt*) {
}

@event
func SignerPublicKeyChanged(new_public_key: felt) {
}

@event
func GuardianPublicKeyChanged(new_public_key: felt) {
}

@event
func SignerEscapeTriggered(active_at: felt) {
}

@event
func SignerEscaped(active_at: felt) {
}

@event
func EscapeCanceled() {
}

//
// Internal functions
//

func assert_only_self{ syscall_ptr : felt* }() {
  let (self) = get_contract_address();
  let (caller) = get_caller_address();
  with_attr error_message("Account: caller is not this account") {
    assert self = caller;
  }
  return ();
}

func assert_non_reentrant{ syscall_ptr: felt* }() {
  let (caller) = get_caller_address();
  with_attr error_message("Account: no reentrant call") {
    assert caller = 0;
  }
  return ();
}

func assert_initialized{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  range_check_ptr
}() {
  let (signer) = Account_signer_public_key.read();
  with_attr error_message("Account: not initialized") {
    assert_not_zero(signer);
  }
  return ();
}

func assert_no_self_call(self: felt, call_array_len: felt, call_array: CallArray*) {
  if (call_array_len == 0) {
    return ();
  }

  assert_not_zero(call_array[0].to - self);
  assert_no_self_call(self, call_array_len - 1, call_array + CallArray.SIZE);
  return ();
}

func assert_guardian_set{
    syscall_ptr: felt*,
    pedersen_ptr: HashBuiltin*,
    range_check_ptr
  }() {
  let (guardian) = Account_guardian_public_key.read();
  with_attr error_message("Account: guardian must be set") {
    assert_not_zero(guardian);
  }
  return ();
}

func assert_correct_tx_version{syscall_ptr: felt*}(tx_version: felt) -> () {
  with_attr error_message("Account: invalid tx version") {
    assert (tx_version - TRANSACTION_VERSION) * (tx_version - QUERY_VERSION) = 0;
  }
  return ();
}

// Executes a list of contract calls recursively.
func execute_calls{syscall_ptr: felt*}(
  calls_len: felt,
  calls: Call*,
  response: felt*
) -> (response_len: felt) {
  alloc_locals;

  // if no more calls
  if (calls_len == 0) {
     return (response_len=0);
  }

  // do the current call
  let this_call: Call = [calls];
  let res = call_contract(
    contract_address=this_call.to,
    function_selector=this_call.selector,
    calldata_size=this_call.calldata_len,
    calldata=this_call.calldata
  );
  // copy the result in response
  memcpy(response, res.retdata, res.retdata_size);
  // do the next calls recursively
  let (response_len) = execute_calls(calls_len - 1, calls + Call.SIZE, response + res.retdata_size);
  return (response_len=response_len + res.retdata_size);
}

func from_call_array_to_call{syscall_ptr: felt*}(
  call_array_len: felt,
  call_array: CallArray*,
  calldata: felt*,
  calls: Call*
) {
  // if no more calls
  if (call_array_len == 0) {
     return ();
  }

  // parse the current call
  assert [calls] = Call(
    to=[call_array].to,
    selector=[call_array].selector,
    calldata_len=[call_array].data_len,
    calldata=calldata + [call_array].data_offset
  );

  // parse the remaining calls recursively
  from_call_array_to_call(call_array_len - 1, call_array + CallArray.SIZE, calldata, calls + Call.SIZE);
  return ();
}

namespace Account {

  //
  // Constants
  //

  const TRIGGER_ESCAPE_SIGNER_SELECTOR = 823970870440803648323000253851988489761099050950583820081611025987402410277;
  const ESCAPE_SIGNER_SELECTOR = 578307412324655990419134484880427622068887477430675222732446709420063579565;
  const SUPPORTS_INTERFACE_SELECTOR = 1184015894760294494673613438913361435336722154500302038630992932234692784845;

  const ESCAPE_SECURITY_PERIOD = 3 * 24 * 60 * 60; // 3 days

  //
  // Initializer
  //

  func initializer{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr
  }(signer_public_key: felt, guardian_public_key: felt) {
    // check that we are not already initialized
    let (current_signer_public_key) = Account_signer_public_key.read();
    with_attr error_message("Account: already initialized") {
        assert current_signer_public_key = 0;
    }

    // check that the target signer is not zero
    with_attr error_message("Account: signer public key cannot be null") {
      assert_not_zero(signer_public_key);
    }

    Account_signer_public_key.write(signer_public_key);
    Account_guardian_public_key.write(guardian_public_key);

    // emit event
    AccountInitialized.emit(signer_public_key, guardian_public_key);
    return ();
  }

  //
  // Getters
  //

  func get_version() -> (version: felt) {
    return (version=VERSION);
  }

  func get_signer_public_key{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr
  }() -> (res: felt) {
    let (res) = Account_signer_public_key.read();
    return (res=res);
  }

  func get_guardian_public_key{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr
  }() -> (res: felt) {
    let (res) = Account_guardian_public_key.read();
    return (res=res);
  }

  func get_signer_escape{
    syscall_ptr: felt*,
    pedersen_ptr: HashBuiltin*,
    range_check_ptr
  }() -> (active_at: felt) {
    let (res) = Account_signer_escape.read();
    return (active_at=res.active_at);
  }

  //
  // Setters
  //

  func set_signer_public_key{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr
  }(new_public_key: felt) {
    // only called via execute
    assert_only_self();

    // check that the target signer is not zero
    with_attr error_message("Account: signer public key cannot be null") {
      assert_not_zero(new_public_key);
    }

    Account_signer_public_key.write(new_public_key);
    SignerPublicKeyChanged.emit(new_public_key);
    return ();
  }

  func set_guardian_public_key{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr
  }(new_public_key: felt) {
    // only called via execute
    assert_only_self();

    Account_guardian_public_key.write(new_public_key);
    GuardianPublicKeyChanged.emit(new_public_key);
    return ();
  }

  func upgrade{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr
  }(implementation: felt) {
    // only called via execute
    assert_only_self();

    // make sure the target is an account
    with_attr error_message("Account: invalid implementation") {
      let (calldata: felt*) = alloc();
      assert calldata[0] = IACCOUNT_ID;

      let (retdata_size: felt, retdata: felt*) = library_call(
        class_hash=implementation,
        function_selector=SUPPORTS_INTERFACE_SELECTOR,
        calldata_size=1,
        calldata=calldata
      );

      assert retdata_size = 1;
      assert [retdata] = TRUE;
    }

    // change implementation
    Proxy.set_implementation(implementation);
    AccountUpgraded.emit(new_implementation=implementation);
    return ();
  }

  //
  // Business logic
  //

  func is_valid_signature{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
    ecdsa_ptr: SignatureBuiltin*
  }(hash: felt, signature_len: felt, signature: felt*) -> (is_valid: felt) {
    let (is_valid) = validate_signer_signature(hash, signature_len, signature);
    return (is_valid=is_valid);
  }

  func supports_interface{
    syscall_ptr: felt*,
    pedersen_ptr: HashBuiltin*,
    range_check_ptr
  }(interface_id: felt) -> (success: felt) {
    // ERC165
    if (interface_id == IERC165_ID) {
      return (success=TRUE);
    }
    // IAccount
    if (interface_id == IACCOUNT_ID) {
      return (success=TRUE);
    }
    // Old IAccount
    if (interface_id == IACCOUNT_ID_OLD) {
      return (success=TRUE);
    }
    return (success=FALSE);
  }

  // Escape

  func trigger_signer_escape{
    syscall_ptr: felt*,
    pedersen_ptr: HashBuiltin*,
    range_check_ptr
  }() {
    // only called via execute
    assert_only_self();
    // no escape when there is no guardian set
    assert_guardian_set();

    // store new escape
    let (block_timestamp) = get_block_timestamp();
    let new_escape: Escape = Escape(block_timestamp + ESCAPE_SECURITY_PERIOD);
    Account_signer_escape.write(new_escape);
    SignerEscapeTriggered.emit(active_at=block_timestamp + ESCAPE_SECURITY_PERIOD);

    return ();
  }

  func cancel_escape{
    syscall_ptr: felt*,
    pedersen_ptr: HashBuiltin*,
    range_check_ptr
  }() {
    // only called via execute
    assert_only_self();

    // validate there is an active escape
    let (current_signer_escape) = Account_signer_escape.read();
    with_attr error_message("Account: no escape to cancel") {
      assert_not_zero(current_signer_escape.active_at);
    }

    // clear escape
    let new_escape: Escape = Escape(0);
    Account_signer_escape.write(new_escape);
    EscapeCanceled.emit();

    return ();
  }

  func escape_signer{
    syscall_ptr: felt*,
    pedersen_ptr: HashBuiltin*,
    range_check_ptr
  }(new_signer_public_key: felt) {
    alloc_locals;

    // only called via execute
    assert_only_self();
    // no escape when the guardian is not set
    assert_guardian_set();

    let (current_signer_escape) = Account_signer_escape.read();
    let (block_timestamp) = get_block_timestamp();
    with_attr error_message("Account: invalid escape") {
      // validate there is an active escape
      assert_not_zero(current_signer_escape.active_at);
      assert_le(current_signer_escape.active_at, block_timestamp);
    }

    // clear escape
    let new_escape: Escape = Escape(0);
    Account_signer_escape.write(new_escape);

    // change signer
    with_attr error_message("Account: new signer public key cannot be null") {
      // check that the target signer is not zero
      assert_not_zero(new_signer_public_key);
    }
    Account_signer_public_key.write(new_signer_public_key);
    SignerEscaped.emit(new_signer_public_key);

    return ();
  }

  //
  // Signatures
  //

  func validate_signer_signature{
    syscall_ptr: felt*,
    pedersen_ptr: HashBuiltin*,
    ecdsa_ptr: SignatureBuiltin*,
    range_check_ptr
  }(message: felt, signatures_len: felt, signatures: felt*) -> (is_valid: felt) {
    with_attr error_message("Account: invalid signer signature") {
      assert_nn(signatures_len - 2);
      let (public_key) = Account_signer_public_key.read();

      verify_ecdsa_signature(
        message=message,
        public_key=public_key,
        signature_r=signatures[0],
        signature_s=signatures[1]
      );
    }

    return (is_valid=TRUE);
  }

  func validate_guardian_signature{
    syscall_ptr: felt*,
    pedersen_ptr: HashBuiltin*,
    ecdsa_ptr: SignatureBuiltin*,
    range_check_ptr
  }(message: felt, signatures_len: felt, signatures: felt*) -> (is_valid: felt) {
    let (public_key) = Account_guardian_public_key.read();

    if (public_key == 0) {
      return (is_valid=TRUE);
    } else {
      with_attr error_message("Account: invalid guardian signature") {
        assert_nn(signatures_len - 2);

        verify_ecdsa_signature(
          message=message,
          public_key=public_key,
          signature_r=signatures[0],
          signature_s=signatures[1]
        );
      }
    }

    return (is_valid=TRUE);
  }
}

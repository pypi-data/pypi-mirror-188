%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin, SignatureBuiltin, BitwiseBuiltin
from starkware.cairo.common.alloc import alloc
from starkware.starknet.common.syscalls import get_tx_info

from periphery.account.library import (
  Account,
  CallArray,
  Call,
  assert_no_self_call,
  assert_initialized,
  assert_non_reentrant,
  assert_correct_tx_version,
  from_call_array_to_call,
  execute_calls,
)

//
// Events
//

@event
func TransactionExecuted(hash: felt, response_len: felt, response: felt*) {
}

//
// Initializer
//

@external
func initialize{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  range_check_ptr
}(signer_public_key: felt, guardian_public_key: felt) {
  Account.initializer(signer_public_key, guardian_public_key);
  return ();
}

//
// Getters
//

@view
func get_version() -> (version: felt) {
  let (version) = Account.get_version();
  return (version=version);
}

@view
func get_signer_public_key{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  range_check_ptr
}() -> (public_key: felt) {
  let (public_key) = Account.get_signer_public_key();
  return (public_key=public_key);
}

@view
func get_guardian_public_key{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  range_check_ptr
}() -> (public_key: felt) {
  let (public_key) = Account.get_guardian_public_key();
  return (public_key=public_key);
}

@view
func get_signer_escape{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  range_check_ptr
}() -> (active_at: felt) {
  let (active_at) = Account.get_signer_escape();
  return (active_at=active_at);
}

@view
func supportsInterface{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  range_check_ptr
}(interfaceId: felt) -> (success: felt) {
  let (success) = Account.supports_interface(interfaceId);
  return (success=success);
}

//
// Setters
//

@external
func set_signer_public_key{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  range_check_ptr
}(new_public_key: felt) {
  Account.set_signer_public_key(new_public_key);
  return ();
}

@external
func set_guardian_public_key{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  range_check_ptr
}(new_public_key: felt) {
  Account.set_guardian_public_key(new_public_key);
  return ();
}

@external
func upgrade{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  range_check_ptr
}(implementation: felt) {
  Account.upgrade(implementation);
  return ();
}

// Escape

@external
func trigger_signer_escape{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  range_check_ptr
}() {
  Account.trigger_signer_escape();
  return ();
}

@external
func cancel_escape{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  range_check_ptr
}() {
  Account.cancel_escape();
  return ();
}

@external
func escape_signer{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  range_check_ptr
}(new_signer_public_key: felt) {
  Account.escape_signer(new_signer_public_key);
  return ();
}

//
// Business logic
//

@view
func isValidSignature{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  range_check_ptr,
  ecdsa_ptr: SignatureBuiltin*
}(hash: felt, signature_len: felt, signature: felt*) -> (isValid: felt) {
  let (isValid: felt) = Account.is_valid_signature(hash, signature_len, signature);
  return (isValid=isValid);
}

@external
func __validate__{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  ecdsa_ptr: SignatureBuiltin*,
  range_check_ptr,
}(call_array_len: felt, call_array: CallArray*, calldata_len: felt, calldata: felt*) {
  alloc_locals;

  // make sure the account is initialized
  assert_initialized();

  // get the tx info
  let (tx_info) = get_tx_info();

  if (call_array_len == 1) {
    if (call_array[0].to == tx_info.account_contract_address) {
      tempvar guardian_condition = (call_array[0].selector - Account.ESCAPE_SIGNER_SELECTOR) * (call_array[0].selector - Account.TRIGGER_ESCAPE_SIGNER_SELECTOR);

      if (guardian_condition == 0) {
        // validate guardian signature
        Account.validate_guardian_signature(tx_info.transaction_hash, tx_info.signature_len, tx_info.signature);
        return ();
      }
    }
  } else {
      // make sure no call is to the account
      assert_no_self_call(tx_info.account_contract_address, call_array_len, call_array);
  }

  // validate signature
  Account.validate_signer_signature(tx_info.transaction_hash, tx_info.signature_len, tx_info.signature);
  return ();
}

@external
func __validate_declare__{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  ecdsa_ptr: SignatureBuiltin*,
  range_check_ptr,
}(class_hash: felt) {
  // make sure the account is initialized
  assert_initialized();

  // get the tx info
  let (tx_info) = get_tx_info();

  // validate signature
  Account.validate_signer_signature(tx_info.transaction_hash, tx_info.signature_len, tx_info.signature);
  return ();
}

@external
func __execute__{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  ecdsa_ptr: SignatureBuiltin*,
  bitwise_ptr: BitwiseBuiltin*,
  range_check_ptr,
}(
  call_array_len: felt,
  call_array: CallArray*,
  calldata_len: felt,
  calldata: felt*
) -> (response_len: felt, response: felt*) {
  alloc_locals;

  // no reentrant call to prevent signature reutilization
  assert_non_reentrant();

  // get the tx info
  let (tx_info) = get_tx_info();

  // block transaction with version != 1 or QUERY
  assert_correct_tx_version(tx_info.version);

  // TMP: Convert `CallArray` to 'Call'.
  let (calls : Call*) = alloc();
  from_call_array_to_call(call_array_len, call_array, calldata, calls);
  let calls_len = call_array_len;

  let (response : felt*) = alloc();
  let (response_len) = execute_calls(calls_len, calls, response);

  // emit event
  TransactionExecuted.emit(hash=tx_info.transaction_hash, response_len=response_len, response=response);
  return (response_len=response_len, response=response);
}

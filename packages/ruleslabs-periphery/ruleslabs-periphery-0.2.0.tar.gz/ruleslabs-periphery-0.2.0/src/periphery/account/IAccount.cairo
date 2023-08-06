%lang starknet

from periphery.account.library import CallArray

@contract_interface
namespace IAccount:

  //
  // Business logic
  //

  func upgrade(
    implementation: felt
  ) -> (response_len: felt, response: felt*) {
  }

  @view
  func isValidSignature{
      syscall_ptr: felt*,
      pedersen_ptr: HashBuiltin*,
      range_check_ptr,
      ecdsa_ptr: SignatureBuiltin*
    }(hash: felt, signature_len: felt, signature: felt*) -> (isValid: felt) {
  }

  func __validate__{
      syscall_ptr: felt*,
      pedersen_ptr: HashBuiltin*,
      ecdsa_ptr: SignatureBuiltin*,
      range_check_ptr,
    }(call_array_len: felt, call_array: CallArray*, calldata_len: felt, calldata: felt*) {
  }

  func __validate_declare__{
    syscall_ptr: felt*,
    pedersen_ptr: HashBuiltin*,
    ecdsa_ptr: SignatureBuiltin*,
    range_check_ptr,
  }(class_hash: felt) {
  }

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
  }
}

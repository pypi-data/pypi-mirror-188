%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin

from periphery.proxy.library import Proxy

//
// Initializer
//

@constructor
func constructor{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  range_check_ptr
}(implementation: felt, selector: felt, calldata_len: felt, calldata: felt*) {
  Proxy.initializer(implementation, selector, calldata_len, calldata);
  return ();
}

//
// Getters
//

@view
func get_implementation{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  range_check_ptr
} () -> (implementation: felt) {
  let (implementation) = Proxy.get_implementation();
  return (implementation=implementation);
}

//
// Business logic
//

@external
@raw_input
@raw_output
func __default__{
  syscall_ptr: felt*,
  pedersen_ptr: HashBuiltin*,
  range_check_ptr
}(selector: felt, calldata_size: felt, calldata: felt*) -> (retdata_size: felt, retdata: felt*) {
  let (retdata_size, retdata) = Proxy.default(selector, calldata_size, calldata);
  return (retdata_size=retdata_size, retdata=retdata);
}

@l1_handler
@raw_input
func __l1_default__{
  syscall_ptr : felt*,
  pedersen_ptr : HashBuiltin*,
  range_check_ptr
}(selector: felt, calldata_size: felt, calldata: felt*) {
  Proxy.l1_default(selector, calldata_size, calldata);
  return ();
}

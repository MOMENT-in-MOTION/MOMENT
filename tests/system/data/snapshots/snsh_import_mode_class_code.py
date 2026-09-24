# --- GENERATED CODE - DO NOT EDIT ---
from __future__ import annotations
from models.addresses import Address, BillingAddress

class Customer():
    """
    Generated dataclass for Customer
    Attributes:
        _customer_name: str        _primary_address: Address        _billing_address: BillingAddress    """
    _customer_name: str
    _primary_address: Address
    _billing_address: BillingAddress

    def __init__(self, customer_name: str, primary_address: Address, billing_address: BillingAddress) -> None:
        """Generated constructor for Customer"""
        if not isinstance(customer_name, str):
            raise TypeError(
                f"Expected 'str' for '_customer_name', got {type(customer_name).__name__!r}"
            )

        self._customer_name = customer_name
        if not isinstance(primary_address, Address):
            raise TypeError(
                f"Expected 'Address' for '_primary_address', got {type(primary_address).__name__!r}"
            )

        self._primary_address = primary_address
        if not isinstance(billing_address, BillingAddress):
            raise TypeError(
                f"Expected 'BillingAddress' for '_billing_address', got {type(billing_address).__name__!r}"
            )

        self._billing_address = billing_address

    def get_customer_name(self) -> str:
        """Generated getter for _customer_name"""
        if self._customer_name is None:
            raise ValueError("Field '_customer_name' has not been initialized.")
        return self._customer_name

    def set_customer_name(self, value: str) -> None:
        """
        Generated setter for _customer_name

        Args:
            value: The new value to assign to the "_customer_name" attribute
        """
        if not isinstance(value, str):
            raise TypeError(
                f"Expected 'str' for '_customer_name', got {type(value).__name__!r}"
            )

        self._customer_name = value

    def has_customer_name(self) -> bool:
        """Generated has function for _customer_name"""
        if self._customer_name is None:
            return False
        return True
    def get_primary_address(self) -> Address:
        """Generated getter for _primary_address"""
        if self._primary_address is None:
            raise ValueError("Field '_primary_address' has not been initialized.")
        return self._primary_address

    def set_primary_address(self, value: Address) -> None:
        """
        Generated setter for _primary_address

        Args:
            value: The new value to assign to the "_primary_address" attribute
        """
        if not isinstance(value, Address):
            raise TypeError(
                f"Expected 'Address' for '_primary_address', got {type(value).__name__!r}"
            )

        self._primary_address = value

    def has_primary_address(self) -> bool:
        """Generated has function for _primary_address"""
        if self._primary_address is None:
            return False
        return True
    def get_billing_address(self) -> BillingAddress:
        """Generated getter for _billing_address"""
        if self._billing_address is None:
            raise ValueError("Field '_billing_address' has not been initialized.")
        return self._billing_address

    def set_billing_address(self, value: BillingAddress) -> None:
        """
        Generated setter for _billing_address

        Args:
            value: The new value to assign to the "_billing_address" attribute
        """
        if not isinstance(value, BillingAddress):
            raise TypeError(
                f"Expected 'BillingAddress' for '_billing_address', got {type(value).__name__!r}"
            )

        self._billing_address = value

    def has_billing_address(self) -> bool:
        """Generated has function for _billing_address"""
        if self._billing_address is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for Customer"""
        result = {}
        result["customer_name"] = (
            self._customer_name.to_dict() if hasattr(self._customer_name, "to_dict")
            else (self._customer_name.value if hasattr(self._customer_name, "value") else self._customer_name)
        )
        result["primary_address"] = (
            self._primary_address.to_dict() if hasattr(self._primary_address, "to_dict")
            else (self._primary_address.value if hasattr(self._primary_address, "value") else self._primary_address)
        )
        result["billing_address"] = (
            self._billing_address.to_dict() if hasattr(self._billing_address, "to_dict")
            else (self._billing_address.value if hasattr(self._billing_address, "value") else self._billing_address)
        )
        return result


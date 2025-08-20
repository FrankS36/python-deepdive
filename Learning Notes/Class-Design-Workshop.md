# Python Class Design Workshop 🏗️
## Building Professional, Thorough Classes

### 🎯 **Workshop Objectives**
By the end of this session, you'll master:
- **Complete class anatomy** and organization
- **Professional naming conventions** (PEP 8 and beyond)
- **Attribute placement** and access patterns
- **Method organization** and documentation
- **Type hints** and modern Python practices
- **Class design patterns** for maintainability

---

## 📋 **Part 1: Class Anatomy & Structure**

### **The Perfect Class Template**

```python
"""
Module docstring: Brief description of the module's purpose.
"""

from __future__ import annotations  # For forward references
from typing import Optional, List, Dict, Any, ClassVar
from datetime import datetime, date
from abc import ABC, abstractmethod
import logging

# Module-level constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3


class ExampleClass:
    """
    One-line summary of the class purpose.
    
    Detailed description of what this class represents and its
    primary responsibilities. Include usage examples if complex.
    
    Attributes:
        class_var: Description of class variable
        
    Example:
        >>> obj = ExampleClass("name", 42)
        >>> obj.process()
        'Processed successfully'
        
    Note:
        Any important notes, limitations, or gotchas.
    """
    
    # 1. CLASS VARIABLES (CONSTANTS FIRST)
    DEFAULT_VALUE: ClassVar[int] = 100
    VALID_TYPES: ClassVar[List[str]] = ['type1', 'type2', 'type3']
    
    # 2. CLASS VARIABLES (MUTABLE - BE CAREFUL)
    _instance_count: ClassVar[int] = 0
    
    # 3. SLOTS (for memory optimization)
    __slots__ = ['_name', '_value', '_created_at', '_status']
    
    def __init__(self, name: str, value: int, *, timeout: Optional[int] = None) -> None:
        """
        Initialize a new ExampleClass instance.
        
        Args:
            name: A descriptive name for this instance
            value: Numeric value to store
            timeout: Optional timeout in seconds (keyword-only)
            
        Raises:
            ValueError: If name is empty or value is negative
            TypeError: If arguments are wrong type
            
        Example:
            >>> obj = ExampleClass("test", 42, timeout=30)
        """
        # 4. INPUT VALIDATION (early and strict)
        if not isinstance(name, str):
            raise TypeError(f"name must be str, got {type(name).__name__}")
        if not name.strip():
            raise ValueError("name cannot be empty")
        if not isinstance(value, int):
            raise TypeError(f"value must be int, got {type(value).__name__}")
        if value < 0:
            raise ValueError("value must be non-negative")
        if timeout is not None and timeout <= 0:
            raise ValueError("timeout must be positive")
        
        # 5. PRIVATE ATTRIBUTES (leading underscore)
        self._name = name.strip()
        self._value = value
        self._created_at = datetime.now()
        self._status = 'initialized'
        self._timeout = timeout or DEFAULT_TIMEOUT
        
        # 6. UPDATE CLASS STATE
        ExampleClass._instance_count += 1
        
        # 7. SETUP LOGGING (if needed)
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._logger.debug(f"Created {self._name} with value {self._value}")
    
    # 8. PROPERTIES (for controlled access)
    @property
    def name(self) -> str:
        """Get the instance name."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Set the instance name with validation."""
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        if not value.strip():
            raise ValueError("name cannot be empty")
        self._name = value.strip()
        self._logger.info(f"Name changed to {self._name}")
    
    @property
    def value(self) -> int:
        """Get the current value."""
        return self._value
    
    @value.setter
    def value(self, new_value: int) -> None:
        """Set the value with validation and logging."""
        if not isinstance(new_value, int):
            raise TypeError("value must be an integer")
        if new_value < 0:
            raise ValueError("value must be non-negative")
        
        old_value = self._value
        self._value = new_value
        self._logger.info(f"Value changed from {old_value} to {new_value}")
    
    @property
    def age_seconds(self) -> float:
        """Get age of this instance in seconds (computed property)."""
        return (datetime.now() - self._created_at).total_seconds()
    
    @property
    def status(self) -> str:
        """Get current status (read-only)."""
        return self._status
    
    # 9. PUBLIC INSTANCE METHODS (alphabetical order)
    def process(self) -> str:
        """
        Process this instance's data.
        
        Returns:
            Success message with processed result
            
        Raises:
            RuntimeError: If instance is not in valid state
            
        Example:
            >>> obj = ExampleClass("test", 42)
            >>> result = obj.process()
            >>> print(result)
            'Processed test: result = 84'
        """
        if self._status != 'initialized':
            raise RuntimeError(f"Cannot process in status '{self._status}'")
        
        try:
            self._status = 'processing'
            result = self._calculate_result()
            self._status = 'completed'
            return f"Processed {self._name}: result = {result}"
        except Exception as e:
            self._status = 'error'
            self._logger.error(f"Processing failed: {e}")
            raise
    
    def reset(self) -> None:
        """Reset instance to initial state."""
        self._status = 'initialized'
        self._logger.info(f"Reset {self._name}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert instance to dictionary representation.
        
        Returns:
            Dictionary with all public attributes
        """
        return {
            'name': self._name,
            'value': self._value,
            'status': self._status,
            'created_at': self._created_at.isoformat(),
            'age_seconds': self.age_seconds
        }
    
    # 10. PRIVATE HELPER METHODS (alphabetical order)
    def _calculate_result(self) -> int:
        """Calculate the processed result (internal logic)."""
        return self._value * 2
    
    def _validate_state(self) -> bool:
        """Validate internal state consistency."""
        return (
            isinstance(self._name, str) and
            isinstance(self._value, int) and
            self._value >= 0 and
            self._status in ['initialized', 'processing', 'completed', 'error']
        )
    
    # 11. CLASS METHODS
    @classmethod
    def create_default(cls, name: str) -> ExampleClass:
        """
        Create instance with default values.
        
        Args:
            name: Instance name
            
        Returns:
            New ExampleClass instance with default value
        """
        return cls(name, cls.DEFAULT_VALUE)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ExampleClass:
        """
        Create instance from dictionary data.
        
        Args:
            data: Dictionary containing 'name' and 'value' keys
            
        Returns:
            New ExampleClass instance
            
        Raises:
            KeyError: If required keys are missing
            ValueError: If data is invalid
        """
        try:
            return cls(
                name=data['name'],
                value=data['value'],
                timeout=data.get('timeout')
            )
        except KeyError as e:
            raise KeyError(f"Missing required key: {e}")
    
    @classmethod
    def get_instance_count(cls) -> int:
        """Get total number of instances created."""
        return cls._instance_count
    
    # 12. STATIC METHODS
    @staticmethod
    def validate_name(name: str) -> bool:
        """
        Validate if a name meets requirements.
        
        Args:
            name: Name to validate
            
        Returns:
            True if valid, False otherwise
        """
        return isinstance(name, str) and len(name.strip()) > 0
    
    @staticmethod
    def calculate_hash(text: str) -> int:
        """Calculate simple hash for text."""
        return hash(text) % 1000000
    
    # 13. MAGIC/DUNDER METHODS (alphabetical order)
    def __bool__(self) -> bool:
        """Return True if instance is in valid state."""
        return self._validate_state() and self._status != 'error'
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on name and value."""
        if not isinstance(other, ExampleClass):
            return NotImplemented
        return self._name == other._name and self._value == other._value
    
    def __hash__(self) -> int:
        """Make instance hashable based on immutable attributes."""
        return hash((self._name, self._value, self._created_at))
    
    def __repr__(self) -> str:
        """Developer-friendly string representation."""
        return (
            f"{self.__class__.__name__}("
            f"name={self._name!r}, "
            f"value={self._value}, "
            f"status={self._status!r})"
        )
    
    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"{self._name} (value: {self._value}, status: {self._status})"
    
    # 14. CONTEXT MANAGER (if applicable)
    def __enter__(self) -> ExampleClass:
        """Enter context manager."""
        self._logger.debug(f"Entering context for {self._name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager."""
        self._logger.debug(f"Exiting context for {self._name}")
        if exc_type is not None:
            self._status = 'error'
            self._logger.error(f"Context exit with error: {exc_val}")
        
    # 15. CLEANUP
    def __del__(self) -> None:
        """Cleanup when instance is garbage collected."""
        self._logger.debug(f"Destroying {self._name}")
```

---

## 🏷️ **Part 2: Naming Conventions Deep Dive**

### **Complete Naming Standards**

```python
class NamingConventionsDemo:
    """Comprehensive demonstration of Python naming conventions."""
    
    # ✅ CLASS NAMES: PascalCase
    # Examples: User, BankAccount, HTTPClient, XMLParser
    
    # ✅ CONSTANTS: SCREAMING_SNAKE_CASE
    MAX_CONNECTIONS = 100
    DEFAULT_TIMEOUT_SECONDS = 30
    API_BASE_URL = "https://api.example.com"
    
    # ✅ CLASS VARIABLES: snake_case
    instance_count = 0
    default_settings = {}
    
    # ✅ PRIVATE CLASS VARIABLES: leading underscore
    _internal_cache = {}
    _debug_mode = False
    
    def __init__(self, user_name: str, email_address: str):
        # ✅ INSTANCE VARIABLES: snake_case
        self.user_name = user_name
        self.email_address = email_address
        self.creation_date = datetime.now()
        self.is_active = True
        
        # ✅ PROTECTED ATTRIBUTES: single leading underscore
        # (convention: "internal use, but subclasses can access")
        self._user_id = self._generate_id()
        self._settings = {}
        
        # ✅ PRIVATE ATTRIBUTES: double leading underscore
        # (triggers name mangling for true privacy)
        self.__password_hash = None
        self.__secret_token = None
    
    # ✅ METHOD NAMES: snake_case, descriptive verbs
    def get_full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def send_email_notification(self, message: str) -> bool:
        """Send email notification to user."""
        pass
    
    def calculate_monthly_fee(self) -> float:
        """Calculate the monthly fee for this user."""
        pass
    
    # ✅ PROTECTED METHODS: single leading underscore
    def _validate_email(self, email: str) -> bool:
        """Internal method to validate email format."""
        pass
    
    def _generate_id(self) -> str:
        """Generate unique user ID."""
        pass
    
    # ✅ PRIVATE METHODS: double leading underscore
    def __encrypt_password(self, password: str) -> str:
        """Encrypt user password (truly private)."""
        pass
    
    # ✅ BOOLEAN METHODS: is_, has_, can_, should_
    def is_premium_user(self) -> bool:
        """Check if user has premium status."""
        pass
    
    def has_valid_subscription(self) -> bool:
        """Check if user has valid subscription."""
        pass
    
    def can_access_feature(self, feature_name: str) -> bool:
        """Check if user can access specific feature."""
        pass
    
    def should_send_reminder(self) -> bool:
        """Determine if reminder should be sent."""
        pass
    
    # ✅ PROPERTY NAMES: noun phrases
    @property
    def full_name(self) -> str:
        """User's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def account_balance(self) -> float:
        """Current account balance."""
        return self._calculate_balance()
    
    @property
    def subscription_status(self) -> str:
        """Current subscription status."""
        return self._subscription.status
```

### **Naming Anti-Patterns to Avoid**

```python
# ❌ BAD NAMING EXAMPLES
class user:  # Should be: User
    pass

class HTTPparser:  # Should be: HTTPParser
    pass

class XMLHttpRequest:  # OK, but consider: XmlHttpRequest

def GetUserName():  # Should be: get_user_name()
    pass

def calculatefee():  # Should be: calculate_fee()
    pass

def check():  # Too vague, should be: check_validity() or is_valid()
    pass

def process_data():  # Vague, should be: parse_json_data() or validate_user_input()
    pass

# ❌ BAD VARIABLE NAMES
d = {}  # Should be: user_data or settings
tmp = calculate_value()  # Should be: calculated_value
flag = True  # Should be: is_valid or should_process
```

---

## 🗂️ **Part 3: Advanced Class Organization**

### **Complex Class with Full Organization**

```python
from __future__ import annotations
from typing import Optional, List, Dict, Any, Union, Protocol, TypeVar, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from contextlib import contextmanager
import logging
import threading
from datetime import datetime, timedelta

# Type definitions
T = TypeVar('T')
UserID = Union[str, int]

# Enums for type safety
class UserStatus(Enum):
    """User account status options."""
    ACTIVE = auto()
    INACTIVE = auto()
    SUSPENDED = auto()
    BANNED = auto()

class Permission(Enum):
    """User permission levels."""
    READ = auto()
    WRITE = auto()
    ADMIN = auto()

# Protocol definitions (interfaces)
class Authenticatable(Protocol):
    """Protocol for objects that can be authenticated."""
    def authenticate(self, credentials: str) -> bool: ...
    def is_authenticated(self) -> bool: ...

class Cacheable(Protocol):
    """Protocol for objects that can be cached."""
    def cache_key(self) -> str: ...
    def serialize(self) -> Dict[str, Any]: ...

# Data classes for structured data
@dataclass(frozen=True)
class UserProfile:
    """Immutable user profile data."""
    first_name: str
    last_name: str
    birth_date: date
    phone: Optional[str] = None
    bio: str = ""
    
    def __post_init__(self):
        """Validate data after initialization."""
        if not self.first_name.strip():
            raise ValueError("First name cannot be empty")
        if not self.last_name.strip():
            raise ValueError("Last name cannot be empty")

@dataclass
class UserSettings:
    """Mutable user settings."""
    theme: str = "light"
    language: str = "en"
    notifications_enabled: bool = True
    timezone: str = "UTC"
    privacy_level: int = field(default=1, metadata={"min": 1, "max": 5})

# Main class with complete organization
class AdvancedUser(Authenticatable, Cacheable):
    """
    Advanced user class demonstrating complete organization.
    
    This class shows proper structure for complex, production-ready classes
    including error handling, logging, thread safety, and comprehensive
    documentation.
    
    Attributes:
        DEFAULT_SETTINGS: Default user settings
        MAX_LOGIN_ATTEMPTS: Maximum failed login attempts
        
    Example:
        >>> user = AdvancedUser("john_doe", "john@example.com")
        >>> user.update_profile("John", "Doe", date(1990, 1, 1))
        >>> user.grant_permission(Permission.WRITE)
        >>> print(user.is_authenticated())
        False
    """
    
    # === CLASS-LEVEL CONFIGURATION ===
    DEFAULT_SETTINGS: ClassVar[Dict[str, Any]] = {
        'theme': 'light',
        'language': 'en',
        'notifications': True
    }
    
    MAX_LOGIN_ATTEMPTS: ClassVar[int] = 3
    SESSION_TIMEOUT: ClassVar[timedelta] = timedelta(hours=24)
    
    # === CLASS STATE ===
    _instances: ClassVar[Dict[UserID, AdvancedUser]] = {}
    _lock: ClassVar[threading.RLock] = threading.RLock()
    
    # === SLOTS FOR MEMORY EFFICIENCY ===
    __slots__ = [
        '_user_id', '_username', '_email', '_status', '_permissions',
        '_profile', '_settings', '_created_at', '_last_login',
        '_failed_attempts', '_session_token', '_logger', '_authenticated'
    ]
    
    def __init__(
        self, 
        username: str, 
        email: str, 
        *,
        user_id: Optional[UserID] = None,
        status: UserStatus = UserStatus.ACTIVE
    ) -> None:
        """
        Initialize advanced user.
        
        Args:
            username: Unique username
            email: User email address
            user_id: Optional custom user ID
            status: Initial user status
            
        Raises:
            ValueError: If username/email invalid
            TypeError: If arguments wrong type
            RuntimeError: If user already exists
        """
        # === VALIDATION ===
        self._validate_init_args(username, email, user_id, status)
        
        # === CORE ATTRIBUTES ===
        self._user_id: UserID = user_id or self._generate_user_id()
        self._username: str = username.strip().lower()
        self._email: str = email.strip().lower()
        self._status: UserStatus = status
        
        # === COLLECTIONS ===
        self._permissions: set[Permission] = {Permission.READ}
        
        # === COMPLEX ATTRIBUTES ===
        self._profile: Optional[UserProfile] = None
        self._settings: UserSettings = UserSettings(**self.DEFAULT_SETTINGS)
        
        # === TIMESTAMPS ===
        self._created_at: datetime = datetime.now()
        self._last_login: Optional[datetime] = None
        
        # === SECURITY ===
        self._failed_attempts: int = 0
        self._session_token: Optional[str] = None
        self._authenticated: bool = False
        
        # === INFRASTRUCTURE ===
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # === REGISTRATION ===
        with self._lock:
            if self._user_id in self._instances:
                raise RuntimeError(f"User {self._user_id} already exists")
            self._instances[self._user_id] = self
        
        self._logger.info(f"Created user {self._username} ({self._user_id})")
    
    # === PROPERTIES ===
    @property
    def user_id(self) -> UserID:
        """Get user ID (immutable)."""
        return self._user_id
    
    @property
    def username(self) -> str:
        """Get username (immutable after creation)."""
        return self._username
    
    @property
    def email(self) -> str:
        """Get email address."""
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        """Set email with validation."""
        if not isinstance(value, str):
            raise TypeError("Email must be string")
        if '@' not in value or '.' not in value:
            raise ValueError("Invalid email format")
        
        old_email = self._email
        self._email = value.strip().lower()
        self._logger.info(f"Email changed from {old_email} to {self._email}")
    
    @property
    def status(self) -> UserStatus:
        """Get user status."""
        return self._status
    
    @status.setter  
    def status(self, value: UserStatus) -> None:
        """Set user status with logging."""
        if not isinstance(value, UserStatus):
            raise TypeError("Status must be UserStatus enum")
        
        old_status = self._status
        self._status = value
        self._logger.warning(f"Status changed from {old_status} to {value}")
    
    @property
    def is_active(self) -> bool:
        """Check if user is active."""
        return self._status == UserStatus.ACTIVE
    
    @property
    def profile(self) -> Optional[UserProfile]:
        """Get user profile."""
        return self._profile
    
    @property
    def settings(self) -> UserSettings:
        """Get user settings (mutable)."""
        return self._settings
    
    @property
    def permissions(self) -> frozenset[Permission]:
        """Get user permissions (immutable view)."""
        return frozenset(self._permissions)
    
    @property
    def account_age_days(self) -> int:
        """Get account age in days."""
        return (datetime.now() - self._created_at).days
    
    # === PUBLIC METHODS ===
    def authenticate(self, password: str) -> bool:
        """
        Authenticate user with password.
        
        Args:
            password: User password to verify
            
        Returns:
            True if authentication successful
            
        Raises:
            ValueError: If too many failed attempts
        """
        if self._failed_attempts >= self.MAX_LOGIN_ATTEMPTS:
            raise ValueError("Too many failed login attempts")
        
        # Simulate password check
        is_valid = self._verify_password(password)
        
        if is_valid:
            self._authenticated = True
            self._failed_attempts = 0
            self._last_login = datetime.now()
            self._session_token = self._generate_session_token()
            self._logger.info(f"User {self._username} authenticated successfully")
        else:
            self._failed_attempts += 1
            self._logger.warning(f"Failed authentication attempt {self._failed_attempts}")
        
        return is_valid
    
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated."""
        if not self._authenticated or not self._session_token:
            return False
        
        # Check session timeout
        if self._last_login and datetime.now() - self._last_login > self.SESSION_TIMEOUT:
            self.logout()
            return False
        
        return True
    
    def logout(self) -> None:
        """Log out user and clear session."""
        self._authenticated = False
        self._session_token = None
        self._logger.info(f"User {self._username} logged out")
    
    def update_profile(
        self, 
        first_name: str, 
        last_name: str, 
        birth_date: date,
        phone: Optional[str] = None,
        bio: str = ""
    ) -> None:
        """Update user profile information."""
        self._profile = UserProfile(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            phone=phone,
            bio=bio
        )
        self._logger.info(f"Profile updated for {self._username}")
    
    def grant_permission(self, permission: Permission) -> None:
        """Grant a permission to the user."""
        if not isinstance(permission, Permission):
            raise TypeError("Permission must be Permission enum")
        
        self._permissions.add(permission)
        self._logger.info(f"Granted {permission.name} to {self._username}")
    
    def revoke_permission(self, permission: Permission) -> None:
        """Revoke a permission from the user."""
        if permission == Permission.READ:
            raise ValueError("Cannot revoke READ permission")
        
        self._permissions.discard(permission)
        self._logger.info(f"Revoked {permission.name} from {self._username}")
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if user has specific permission."""
        return permission in self._permissions
    
    def update_settings(self, **kwargs) -> None:
        """Update user settings."""
        for key, value in kwargs.items():
            if hasattr(self._settings, key):
                setattr(self._settings, key, value)
            else:
                raise ValueError(f"Unknown setting: {key}")
        
        self._logger.debug(f"Settings updated for {self._username}")
    
    def cache_key(self) -> str:
        """Generate cache key for this user."""
        return f"user:{self._user_id}:{hash(self._email)}"
    
    def serialize(self) -> Dict[str, Any]:
        """Serialize user to dictionary."""
        return {
            'user_id': self._user_id,
            'username': self._username,
            'email': self._email,
            'status': self._status.name,
            'permissions': [p.name for p in self._permissions],
            'settings': {
                'theme': self._settings.theme,
                'language': self._settings.language,
                'notifications_enabled': self._settings.notifications_enabled
            },
            'created_at': self._created_at.isoformat(),
            'last_login': self._last_login.isoformat() if self._last_login else None
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        import json
        return json.dumps(self.serialize(), indent=2)
    
    # === PRIVATE METHODS ===
    def _validate_init_args(
        self, 
        username: str, 
        email: str, 
        user_id: Optional[UserID], 
        status: UserStatus
    ) -> None:
        """Validate initialization arguments."""
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Username must be non-empty string")
        if not isinstance(email, str) or '@' not in email:
            raise ValueError("Invalid email address")
        if user_id is not None and not isinstance(user_id, (str, int)):
            raise TypeError("user_id must be string or integer")
        if not isinstance(status, UserStatus):
            raise TypeError("status must be UserStatus enum")
    
    def _generate_user_id(self) -> str:
        """Generate unique user ID."""
        import uuid
        return str(uuid.uuid4())
    
    def _generate_session_token(self) -> str:
        """Generate session token."""
        import secrets
        return secrets.token_urlsafe(32)
    
    def _verify_password(self, password: str) -> bool:
        """Verify password (simplified for demo)."""
        # In real implementation, use proper password hashing
        return len(password) >= 8
    
    # === CLASS METHODS ===
    @classmethod
    def get_user_by_id(cls, user_id: UserID) -> Optional[AdvancedUser]:
        """Get user by ID."""
        with cls._lock:
            return cls._instances.get(user_id)
    
    @classmethod
    def get_user_by_username(cls, username: str) -> Optional[AdvancedUser]:
        """Get user by username."""
        username = username.lower()
        with cls._lock:
            for user in cls._instances.values():
                if user._username == username:
                    return user
        return None
    
    @classmethod
    def get_all_users(cls) -> List[AdvancedUser]:
        """Get all users."""
        with cls._lock:
            return list(cls._instances.values())
    
    @classmethod
    def create_admin_user(cls, username: str, email: str) -> AdvancedUser:
        """Create user with admin permissions."""
        user = cls(username, email)
        user.grant_permission(Permission.WRITE)
        user.grant_permission(Permission.ADMIN)
        return user
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AdvancedUser:
        """Create user from dictionary data."""
        user = cls(
            username=data['username'],
            email=data['email'],
            user_id=data.get('user_id'),
            status=UserStatus[data.get('status', 'ACTIVE')]
        )
        
        # Restore permissions
        for perm_name in data.get('permissions', []):
            user.grant_permission(Permission[perm_name])
        
        # Restore settings
        if 'settings' in data:
            user.update_settings(**data['settings'])
        
        return user
    
    # === STATIC METHODS ===
    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username format."""
        return (
            isinstance(username, str) and
            3 <= len(username.strip()) <= 50 and
            username.isalnum()
        )
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    # === MAGIC METHODS ===
    def __str__(self) -> str:
        """User-friendly string representation."""
        name = f"{self._profile.first_name} {self._profile.last_name}" if self._profile else self._username
        return f"{name} ({self._email})"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return (
            f"{self.__class__.__name__}("
            f"user_id={self._user_id!r}, "
            f"username={self._username!r}, "
            f"email={self._email!r}, "
            f"status={self._status.name})"
        )
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on user ID."""
        if not isinstance(other, AdvancedUser):
            return NotImplemented
        return self._user_id == other._user_id
    
    def __hash__(self) -> int:
        """Make hashable based on user ID."""
        return hash(self._user_id)
    
    def __bool__(self) -> bool:
        """Return True if user is active."""
        return self._status == UserStatus.ACTIVE
    
    # === CONTEXT MANAGER ===
    @contextmanager
    def temporary_permissions(self, *permissions: Permission):
        """Context manager for temporary permissions."""
        original_perms = self._permissions.copy()
        try:
            for perm in permissions:
                self._permissions.add(perm)
            yield self
        finally:
            self._permissions = original_perms
    
    # === CLEANUP ===
    def __del__(self) -> None:
        """Cleanup when user is destroyed."""
        with self._lock:
            self._instances.pop(self._user_id, None)
        self._logger.debug(f"User {self._username} destroyed")
```

---

## 🎯 **Part 4: Key Takeaways & Best Practices**

### **Class Organization Checklist**

```python
# ✅ COMPLETE CLASS STRUCTURE CHECKLIST

class MyClass:
    """
    📋 1. DOCSTRING (always first)
    - One-line summary
    - Detailed description
    - Attributes list
    - Usage examples
    - Important notes
    """
    
    # 📋 2. CLASS VARIABLES (in order)
    CONSTANTS: ClassVar[type] = value     # Constants first
    class_variables: ClassVar[type] = {}  # Then class state
    
    # 📋 3. SLOTS (if using)
    __slots__ = ['attr1', '_attr2']
    
    def __init__(self, ...):
        """📋 4. CONSTRUCTOR with validation"""
        # Input validation first
        # Then attribute initialization
        # Then setup/registration
    
    # 📋 5. PROPERTIES (alphabetical)
    @property
    def attribute(self): ...
    
    # 📋 6. PUBLIC METHODS (alphabetical)
    def method_a(self): ...
    def method_z(self): ...
    
    # 📋 7. PRIVATE METHODS (alphabetical)
    def _helper_method(self): ...
    
    # 📋 8. CLASS METHODS
    @classmethod
    def from_something(cls): ...
    
    # 📋 9. STATIC METHODS
    @staticmethod
    def utility_function(): ...
    
    # 📋 10. MAGIC METHODS (common order)
    def __str__(self): ...
    def __repr__(self): ...
    def __eq__(self): ...
    def __hash__(self): ...
    def __bool__(self): ...
    
    # 📋 11. CONTEXT MANAGER (if applicable)
    def __enter__(self): ...
    def __exit__(self): ...
    
    # 📋 12. CLEANUP
    def __del__(self): ...
```

### **Professional Tips**

1. **🎯 Single Responsibility**: Each class should have one clear purpose
2. **🔒 Encapsulation**: Use private attributes with public interfaces
3. **📝 Documentation**: Every public method needs docstring
4. **⚡ Type Hints**: Use them everywhere for better IDE support
5. **🛡️ Validation**: Validate inputs early and thoroughly
6. **🪵 Logging**: Add structured logging for debugging
7. **🧪 Testability**: Design with testing in mind
8. **⚙️ Configuration**: Use class variables for settings
9. **🏗️ Consistency**: Follow the same patterns throughout
10. **🔄 Immutability**: Prefer immutable data when possible

This workshop gives you the foundation to build robust, maintainable Python classes that follow professional standards! 🚀 

---

## 🧠 **Part 4: Method Binding Design Decisions**

### **Method Binding Decision Tree**

```
📋 CHOOSING THE RIGHT METHOD TYPE

Do you need access to instance data (self)?
├─ YES → Instance Method
│   └─ @property if accessing/computing single value
│   └─ Regular method if performing actions/operations
│
└─ NO → Do you need access to class data (cls)?
    ├─ YES → Class Method (@classmethod)
    │   ├─ Alternative constructors
    │   ├─ Factory methods
    │   ├─ Class configuration
    │   └─ Operations on class attributes
    │
    └─ NO → Static Method (@staticmethod)
        ├─ Utility functions related to the class
        ├─ Validation helpers
        ├─ Pure functions that belong logically to the class
        └─ Helper functions that don't need class/instance data
```

### **Detailed Method Binding Guide**

```python
class MethodBindingExamples:
    """Comprehensive examples of when to use each method type."""
    
    # Class variables for demonstration
    total_instances = 0
    default_config = {'theme': 'dark', 'lang': 'en'}
    
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value
        MethodBindingExamples.total_instances += 1
    
    # ========================================
    # INSTANCE METHODS - Use when you need 'self'
    # ========================================
    
    def calculate_score(self) -> int:
        """
        ✅ INSTANCE METHOD - Needs instance data
        
        Use when:
        - Method operates on instance attributes
        - Method modifies instance state
        - Method needs access to other instance methods
        """
        return self.value * len(self.name)
    
    def update_value(self, new_value: int) -> None:
        """
        ✅ INSTANCE METHOD - Modifies instance state
        
        Use when:
        - Changing instance attributes
        - Method behavior depends on current instance state
        """
        old_value = self.value
        self.value = new_value
        print(f"Updated {self.name} from {old_value} to {new_value}")
    
    def is_high_value(self) -> bool:
        """
        ✅ INSTANCE METHOD - Boolean check on instance data
        
        Use when:
        - Checking instance state/conditions
        - Method returns info about THIS specific instance
        """
        return self.value > 100
    
    @property
    def display_name(self) -> str:
        """
        ✅ PROPERTY - Computed value from instance data
        
        Use when:
        - Accessing computed values that feel like attributes
        - Value depends on instance state
        - Want attribute-like access (no parentheses)
        """
        return f"{self.name.title()} ({self.value})"
    
    # ========================================
    # CLASS METHODS - Use when you need 'cls' but not 'self'
    # ========================================
    
    @classmethod
    def create_default(cls, name: str) -> 'MethodBindingExamples':
        """
        ✅ CLASS METHOD - Alternative constructor
        
        Use when:
        - Creating instances with predefined values
        - Factory methods that return instances of the class
        - Need to access class attributes during construction
        """
        return cls(name, value=0)  # Using cls ensures subclass compatibility
    
    @classmethod
    def create_from_string(cls, data: str) -> 'MethodBindingExamples':
        """
        ✅ CLASS METHOD - Factory method
        
        Use when:
        - Parsing/converting data into instances
        - Alternative ways to create instances
        - Complex construction logic
        """
        parts = data.split(':')
        if len(parts) != 2:
            raise ValueError("Format must be 'name:value'")
        
        name, value_str = parts
        try:
            value = int(value_str)
        except ValueError:
            raise ValueError("Value must be numeric")
        
        return cls(name.strip(), value)
    
    @classmethod
    def get_instance_count(cls) -> int:
        """
        ✅ CLASS METHOD - Access class data
        
        Use when:
        - Returning information about the class itself
        - Operating on class variables
        - Method applies to ALL instances, not one specific instance
        """
        return cls.total_instances
    
    @classmethod
    def update_default_config(cls, **kwargs) -> None:
        """
        ✅ CLASS METHOD - Modify class state
        
        Use when:
        - Changing class-level configuration
        - Updates affect all future instances
        - Managing shared state
        """
        cls.default_config.update(kwargs)
        print(f"Updated default config: {cls.default_config}")
    
    @classmethod
    def create_batch(cls, names: List[str], base_value: int = 0) -> List['MethodBindingExamples']:
        """
        ✅ CLASS METHOD - Factory for multiple instances
        
        Use when:
        - Creating multiple instances at once
        - Batch operations that return instances
        - Complex factory logic
        """
        return [cls(name, base_value + i * 10) for i, name in enumerate(names)]
    
    # ========================================
    # STATIC METHODS - Use when you need neither 'cls' nor 'self'
    # ========================================
    
    @staticmethod
    def validate_name(name: str) -> bool:
        """
        ✅ STATIC METHOD - Pure validation function
        
        Use when:
        - Utility function related to the class concept
        - No need for class or instance data
        - Could be a regular function but belongs logically here
        - Pure function (same input always gives same output)
        """
        return isinstance(name, str) and 2 <= len(name.strip()) <= 50
    
    @staticmethod
    def parse_value_string(value_str: str) -> int:
        """
        ✅ STATIC METHOD - Data conversion utility
        
        Use when:
        - Helper function for data processing
        - Doesn't need class/instance context
        - Could be used before instance creation
        """
        try:
            # Remove common prefixes/suffixes
            cleaned = value_str.strip().replace('$', '').replace(',', '')
            return int(cleaned)
        except ValueError:
            raise ValueError(f"Cannot parse '{value_str}' as integer")
    
    @staticmethod
    def calculate_hash(text: str, salt: str = "default") -> str:
        """
        ✅ STATIC METHOD - Utility function
        
        Use when:
        - Reusable utility that fits thematically with the class
        - No dependency on class/instance state
        - Could be used by other classes or functions
        """
        import hashlib
        return hashlib.sha256(f"{text}{salt}".encode()).hexdigest()[:16]
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """
        ✅ STATIC METHOD - Formatting utility
        
        Use when:
        - Common formatting needs related to the class
        - No state dependencies
        - Reusable across different contexts
        """
        return f"${amount:,.2f}"
```

### **Real-World Decision Examples**

```python
class BankAccount:
    """Real-world examples of method binding decisions."""
    
    # Class configuration
    MINIMUM_BALANCE = 0
    DEFAULT_CURRENCY = "USD"
    _account_counter = 0
    
    def __init__(self, owner: str, initial_balance: float = 0):
        self.owner = owner
        self._balance = initial_balance
        self.account_number = self._generate_account_number()
        BankAccount._account_counter += 1
    
    # ================================
    # INSTANCE METHODS - Account Operations
    # ================================
    
    def deposit(self, amount: float) -> None:
        """❓ WHY INSTANCE METHOD? Modifies THIS account's balance."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
    
    def withdraw(self, amount: float) -> None:
        """❓ WHY INSTANCE METHOD? Modifies THIS account's state."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self._balance - amount < self.MINIMUM_BALANCE:
            raise ValueError("Insufficient funds")
        self._balance -= amount
    
    def transfer_to(self, other_account: 'BankAccount', amount: float) -> None:
        """❓ WHY INSTANCE METHOD? Operates on THIS account (source)."""
        self.withdraw(amount)  # Remove from this account
        other_account.deposit(amount)  # Add to other account
    
    @property
    def balance(self) -> float:
        """❓ WHY PROPERTY? Read-only access to instance data."""
        return self._balance
    
    @property
    def is_overdrawn(self) -> bool:
        """❓ WHY PROPERTY? Computed boolean from instance state."""
        return self._balance < 0
    
    # ================================
    # CLASS METHODS - Account Creation & Management
    # ================================
    
    @classmethod
    def create_savings_account(cls, owner: str, initial_deposit: float = 1000) -> 'BankAccount':
        """
        ❓ WHY CLASS METHOD? 
        - Alternative constructor
        - Uses class to create instance (works with subclasses)
        - Applies business logic for specific account type
        """
        if initial_deposit < 1000:
            raise ValueError("Savings account requires minimum $1000 deposit")
        return cls(owner, initial_deposit)
    
    @classmethod
    def create_from_csv_row(cls, csv_row: str) -> 'BankAccount':
        """
        ❓ WHY CLASS METHOD?
        - Factory method for data import
        - Creates instance from external data format
        - Handles parsing logic
        """
        parts = csv_row.strip().split(',')
        if len(parts) != 2:
            raise ValueError("CSV row must have format: owner,balance")
        
        owner, balance_str = parts
        balance = float(balance_str)
        return cls(owner.strip(), balance)
    
    @classmethod
    def get_total_accounts(cls) -> int:
        """
        ❓ WHY CLASS METHOD?
        - Returns information about ALL accounts (class-level data)
        - Not specific to any one instance
        - Accesses class variable
        """
        return cls._account_counter
    
    @classmethod
    def set_minimum_balance(cls, new_minimum: float) -> None:
        """
        ❓ WHY CLASS METHOD?
        - Changes policy for ALL accounts
        - Modifies class-level configuration
        - Affects future instance behavior
        """
        cls.MINIMUM_BALANCE = new_minimum
        print(f"Minimum balance updated to {cls.DEFAULT_CURRENCY} {new_minimum}")
    
    # ================================
    # STATIC METHODS - Utilities & Validation
    # ================================
    
    @staticmethod
    def validate_owner_name(name: str) -> bool:
        """
        ❓ WHY STATIC METHOD?
        - Pure validation function
        - No dependency on class/instance data
        - Could be used before creating account
        - Belongs logically with BankAccount concept
        """
        return (
            isinstance(name, str) and
            2 <= len(name.strip()) <= 100 and
            name.strip().replace(' ', '').isalpha()
        )
    
    @staticmethod
    def calculate_interest(principal: float, rate: float, years: float) -> float:
        """
        ❓ WHY STATIC METHOD?
        - Mathematical utility related to banking
        - No need for class/instance context
        - Pure function (deterministic)
        - Could be reused by other banking classes
        """
        return principal * (1 + rate) ** years
    
    @staticmethod
    def format_account_number(number: int) -> str:
        """
        ❓ WHY STATIC METHOD?
        - Formatting utility for display
        - Works with any account number
        - No state dependencies
        - Could be used in reports, UI, etc.
        """
        return f"{number:08d}"  # Pad to 8 digits
    
    @staticmethod
    def parse_currency_string(currency_str: str) -> float:
        """
        ❓ WHY STATIC METHOD?
        - Data parsing utility
        - Could be used in CSV import, user input, etc.
        - No dependency on account state
        - Reusable across different contexts
        """
        # Remove currency symbols and commas
        cleaned = currency_str.replace('$', '').replace(',', '').strip()
        try:
            return float(cleaned)
        except ValueError:
            raise ValueError(f"Cannot parse '{currency_str}' as currency amount")
    
    # ================================
    # PRIVATE HELPER METHODS
    # ================================
    
    def _generate_account_number(self) -> int:
        """
        ❓ WHY INSTANCE METHOD (PRIVATE)?
        - Used during instance creation
        - Could potentially use instance data for generation
        - Part of instance initialization process
        """
        return 10000000 + BankAccount._account_counter
    
    # ================================
    # MAGIC METHODS
    # ================================
    
    def __str__(self) -> str:
        """❓ WHY INSTANCE METHOD? Returns string representation of THIS instance."""
        return f"Account({self.owner}: {self.format_currency(self._balance)})"
    
    def __repr__(self) -> str:
        """❓ WHY INSTANCE METHOD? Developer representation of THIS instance."""
        return f"BankAccount(owner={self.owner!r}, initial_balance={self._balance})"
    
    def __eq__(self, other: object) -> bool:
        """❓ WHY INSTANCE METHOD? Compares THIS instance with another."""
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.account_number == other.account_number
```

### **Method Binding Anti-Patterns**

```python
class MethodBindingAntiPatterns:
    """Examples of common mistakes in method binding decisions."""
    
    total_instances = 0
    
    def __init__(self, name: str):
        self.name = name
        MethodBindingAntiPatterns.total_instances += 1
    
    # ❌ ANTI-PATTERN: Using instance method when static would be better
    def validate_email_wrong(self, email: str) -> bool:
        """
        ❌ BAD: This doesn't use 'self' at all!
        Should be @staticmethod since it's a pure validation function.
        """
        return '@' in email and '.' in email
    
    # ✅ CORRECT: Static method for validation
    @staticmethod
    def validate_email_correct(email: str) -> bool:
        """✅ GOOD: Pure validation function."""
        return '@' in email and '.' in email
    
    # ❌ ANTI-PATTERN: Using static method when class method needed
    @staticmethod
    def get_instance_count_wrong() -> int:
        """
        ❌ BAD: Accesses class variable but doesn't use cls!
        This breaks inheritance - subclasses will always return parent's count.
        """
        return MethodBindingAntiPatterns.total_instances
    
    # ✅ CORRECT: Class method for class data access
    @classmethod
    def get_instance_count_correct(cls) -> int:
        """✅ GOOD: Uses cls to access class variable."""
        return cls.total_instances
    
    # ❌ ANTI-PATTERN: Using class method when instance method needed
    @classmethod
    def get_my_name_wrong(cls) -> str:
        """
        ❌ BAD: Trying to access instance data from class method!
        This will fail because cls doesn't have instance attributes.
        """
        # return cls.name  # This would fail!
        return "Unknown"  # Forced to return generic value
    
    # ✅ CORRECT: Instance method for instance data
    def get_my_name_correct(self) -> str:
        """✅ GOOD: Uses self to access instance data."""
        return self.name
    
    # ❌ ANTI-PATTERN: Using property when regular method is better
    @property
    def perform_complex_calculation_wrong(self) -> int:
        """
        ❌ BAD: Heavy computation in a property!
        Properties should be lightweight and feel like attributes.
        """
        # Simulate expensive operation
        result = 0
        for i in range(1000000):
            result += i * len(self.name)
        return result
    
    # ✅ CORRECT: Regular method for complex operations
    def perform_complex_calculation_correct(self) -> int:
        """✅ GOOD: Complex operation as regular method."""
        result = 0
        for i in range(1000000):
            result += i * len(self.name)
        return result
    
    # ❌ ANTI-PATTERN: Creating unnecessary instance just to call method
    def utility_function_wrong(self) -> str:
        """
        ❌ BAD: This could be static but forces instance creation!
        User would need to create instance just to call this utility.
        """
        return "Some utility result that doesn't need instance data"
    
    # ✅ CORRECT: Static method for utilities
    @staticmethod
    def utility_function_correct() -> str:
        """✅ GOOD: Can be called without creating instance."""
        return "Some utility result that doesn't need instance data"
```

### **Design Decision Checklist**

```python
"""
🎯 METHOD BINDING DECISION CHECKLIST

Before writing a method, ask yourself:

1. ❓ Does this method need access to instance attributes (self.attribute)?
   ├─ YES → Instance Method
   └─ NO → Continue to question 2

2. ❓ Does this method need access to class attributes (cls.attribute)?
   ├─ YES → Class Method (@classmethod)
   └─ NO → Continue to question 3

3. ❓ Is this method creating instances of the class?
   ├─ YES → Class Method (@classmethod) - Alternative constructor
   └─ NO → Continue to question 4

4. ❓ Does this method operate on or return class-level information?
   ├─ YES → Class Method (@classmethod)
   └─ NO → Continue to question 5

5. ❓ Is this method a utility function that belongs logically with this class?
   ├─ YES → Static Method (@staticmethod)
   └─ NO → Consider if it should be a regular function outside the class

SPECIAL CASES:

📊 Property vs Method:
- Use @property for: Simple attribute access, computed values, lightweight operations
- Use method for: Actions, complex operations, operations with side effects

🔧 Instance Method Variations:
- Regular method: Actions, operations, modifications
- Property getter: Read-only computed values
- Property setter: Controlled attribute modification
- Property deleter: Custom cleanup when attribute deleted

🏭 Class Method Variations:
- Alternative constructors: Different ways to create instances
- Factory methods: Complex instance creation logic
- Class configuration: Changing class-level settings
- Class introspection: Getting information about the class

⚡ Static Method Variations:
- Validation functions: Input checking/sanitization
- Utility functions: Helper functions related to class concept
- Pure functions: Mathematical operations, formatting
- Conversion functions: Data transformation utilities
"""
```

### **Advanced Binding Patterns**

```python
from typing import Type, TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T', bound='BaseRepository')

class AdvancedBindingPatterns:
    """Advanced patterns for method binding decisions."""
    
    @classmethod
    def create_polymorphic_factory(cls: Type[T]) -> T:
        """
        ✅ ADVANCED: Polymorphic factory with proper typing
        
        Why class method?
        - Works correctly with inheritance
        - Returns instance of the actual class (not base class)
        - Proper type hints for subclasses
        """
        return cls()
    
    @staticmethod
    def dependency_injection_helper(config: dict) -> 'SomeService':
        """
        ✅ ADVANCED: Dependency injection factory
        
        Why static method?
        - Creates instances based on configuration
        - Doesn't belong to any specific class
        - Could create instances of different classes
        - Pure factory function
        """
        service_type = config.get('type', 'default')
        if service_type == 'redis':
            return RedisService(config)
        elif service_type == 'memory':
            return MemoryService(config)
        else:
            return DefaultService(config)
    
    def fluent_interface_method(self) -> 'AdvancedBindingPatterns':
        """
        ✅ ADVANCED: Fluent interface pattern
        
        Why instance method returning self?
        - Allows method chaining
        - Modifies instance state
        - Returns self for continued operations
        """
        # Perform some operation
        return self  # Enable chaining
    
    @property
    def lazy_computed_property(self) -> str:
        """
        ✅ ADVANCED: Lazy loading with caching
        
        Why property with caching?
        - Expensive computation done only once
        - Appears as simple attribute access
        - Automatic memoization
        """
        if not hasattr(self, '_cached_result'):
            # Expensive computation here
            self._cached_result = "Expensive result"
        return self._cached_result
```

This comprehensive method binding section provides clear decision-making frameworks and real-world examples to help you choose the right method type every time! 🎯

---

## 📚 **Comprehensive Glossary**

### **A**

**Abstract Class**: A class that cannot be instantiated directly and typically contains one or more abstract methods that must be implemented by subclasses. Defined using `ABC` (Abstract Base Class) from the `abc` module.

**Abstract Method**: A method declared in an abstract class that has no implementation and must be overridden by subclasses. Marked with `@abstractmethod` decorator.

**Access Modifier**: Symbols indicating the intended visibility/accessibility of class attributes and methods (`+` public, `-` private, `#` protected, `~` package).

**Aggregation**: A "has-a" relationship where the contained objects can exist independently of the container. Weaker form of composition (diamond symbol ◇ in UML).

**Attribute**: A variable that belongs to a class or instance. Can be data (storing values) or callable (methods/functions).

**Attribute Lookup**: The process Python uses to find attributes, following a specific order: instance `__dict__` → class `__dict__` → parent classes (MRO) → `AttributeError`.

### **B**

**Binding**: The process of connecting a function to an object, creating a method. Instance methods are automatically bound to `self` when accessed through an instance.

**Bound Method**: A method that is automatically connected to a specific instance, with `self` pre-filled. Created when accessing an instance method through an instance.

### **C**

**Cache/Caching**: Storing computed results to avoid recalculation. Often used in properties to improve performance for expensive operations.

**Class Attribute**: A variable that belongs to the class itself, shared by all instances. Defined in the class body outside any method.

**Class Method**: A method that receives the class (`cls`) as its first argument instead of an instance. Decorated with `@classmethod`. Used for alternative constructors and class-level operations.

**Class Variable**: Same as class attribute. A variable stored in the class namespace, accessible by all instances.

**ClassVar**: A type hint from the `typing` module indicating that an attribute is a class variable, not an instance variable.

**Composition**: A "part-of" relationship where contained objects cannot exist without the container. Stronger form of aggregation (filled diamond ◆ in UML).

**Context Manager**: An object that defines what happens when entering and exiting a `with` statement. Implements `__enter__` and `__exit__` methods.

### **D**

**Data Class**: A class automatically generated from type annotations using the `@dataclass` decorator. Provides `__init__`, `__repr__`, `__eq__` methods automatically.

**Decorator**: A function that modifies or wraps another function or class. Applied using `@decorator_name` syntax above the target.

**Dependency Injection**: A design pattern where dependencies are provided to an object rather than created by the object itself.

**Descriptor**: An object that defines how attribute access is handled through `__get__`, `__set__`, and `__delete__` methods. Properties are implemented using descriptors.

**Duck Typing**: A programming concept where the type/class of an object is less important than the methods it defines. "If it walks like a duck and quacks like a duck, it's a duck."

**Dunder Methods**: Methods with double underscores before and after the name (e.g., `__init__`, `__str__`). Also called "magic methods" or "special methods."

### **E**

**Encapsulation**: The bundling of data and methods that operate on that data within a single unit (class), often with restricted access to internal details.

**Enum**: A set of named constants defined using the `Enum` class from the `enum` module. Provides type safety and prevents invalid values.

### **F**

**Factory Method**: A class method that creates and returns instances of the class, often with specific configurations or from different data sources.

**Fluent Interface**: A design pattern that allows method chaining by having methods return `self` or the object being configured.

**Forward Reference**: A string-based type annotation that refers to a class not yet defined. Enabled by `from __future__ import annotations`.

**Function**: A standalone callable object not bound to any class or instance.

### **G**

**Getter**: A method (often a property) that retrieves the value of an attribute, potentially with validation or computation.

### **H**

**Hashable**: An object that has a hash value which never changes during its lifetime. Required for use as dictionary keys or set elements.

### **I**

**Immutable**: An object whose state cannot be changed after creation. Examples: strings, tuples, frozen dataclasses.

**Inheritance**: A mechanism where a class (child/subclass) derives attributes and methods from another class (parent/superclass).

**Instance**: A specific object created from a class. Each instance has its own copy of instance attributes.

**Instance Attribute**: A variable that belongs to a specific instance of a class. Each instance has its own copy.

**Instance Method**: A method that operates on a specific instance, automatically receiving `self` as the first argument.

### **L**

**Lazy Loading**: A design pattern where computation or resource loading is deferred until actually needed, improving performance.

### **M**

**Magic Methods**: See "Dunder Methods." Special methods that define how objects behave with built-in operations.

**Mappingproxy**: A read-only view of a dictionary. Used for class `__dict__` to prevent direct modification while allowing attribute access.

**Metaclass**: A class whose instances are classes themselves. Controls class creation and behavior. Most classes use `type` as their metaclass.

**Method**: A function defined inside a class. Can be instance, class, or static methods.

**Method Resolution Order (MRO)**: The order in which Python searches for methods in class hierarchies, especially with multiple inheritance.

**Mixin**: A class designed to be inherited alongside other classes to provide specific functionality. Usually not instantiated directly.

**Monkey Patching**: Dynamically modifying a class or module at runtime by adding, modifying, or deleting attributes.

**Multiplicity**: In UML, indicates how many instances of one class relate to instances of another class (e.g., 1, 0..1, *, 1..*).

**Mutable**: An object whose state can be changed after creation. Examples: lists, dictionaries, most custom objects.

### **N**

**Name Mangling**: Python's mechanism for making attributes "private" by prefixing with double underscore. Renames `__attr` to `_ClassName__attr`.

**Namespace**: A container that holds names (identifiers) and their corresponding objects. Classes and instances have their own namespaces.

### **P**

**PascalCase**: A naming convention where each word starts with a capital letter and no separators are used. Used for class names (e.g., `MyClass`, `HTTPClient`).

**Polymorphism**: The ability of different objects to respond to the same interface/method calls in their own specific way.

**Property**: A special kind of attribute that uses methods (getter/setter/deleter) but appears as a regular attribute to users.

**Protocol**: A way to define interfaces in Python using structural subtyping. Objects that implement the required methods automatically satisfy the protocol.

### **S**

**Setter**: A method (often a property setter) that sets the value of an attribute, potentially with validation.

**Shadowing**: When an instance attribute has the same name as a class attribute, the instance attribute "shadows" (hides) the class attribute for that instance.

**Single Responsibility Principle**: A design principle stating that a class should have only one reason to change, focusing on a single functionality.

**Slots**: A mechanism (`__slots__`) to restrict the attributes an instance can have and reduce memory usage.

**snake_case**: A naming convention using lowercase letters with underscores separating words. Used for variables, functions, and methods (e.g., `my_variable`, `calculate_total`).

**Static Method**: A method that belongs to a class but doesn't receive `self` or `cls` automatically. Decorated with `@staticmethod`. Behaves like a regular function.

**Stereotype**: In UML, additional information about a model element enclosed in guillemets (e.g., `<<abstract>>`, `<<interface>>`).

**SCREAMING_SNAKE_CASE**: A naming convention using uppercase letters with underscores. Used for constants (e.g., `MAX_SIZE`, `DEFAULT_TIMEOUT`).

### **T**

**Type Hint**: Annotations that specify the expected types of variables, parameters, and return values. Improves code readability and enables static analysis.

**TypeVar**: A type variable used in generic programming to represent a type that will be specified later.

### **U**

**UML (Unified Modeling Language)**: A standardized modeling language used to visualize software design, including class diagrams.

**Unbound Method**: A function accessed from a class rather than an instance. In Python 3, these are just regular functions.

### **V**

**Validation**: The process of checking that data meets certain criteria before accepting or processing it.

### **Common Symbols & Abbreviations**

- **`cls`**: Conventional name for the class parameter in class methods
- **`self`**: Conventional name for the instance parameter in instance methods
- **`@`**: Decorator syntax prefix
- **`*args`**: Variable positional arguments
- **`**kwargs`**: Variable keyword arguments
- **`->` **: Return type annotation syntax
- **`:`**: Type annotation syntax for parameters and variables
- **`_`**: Single underscore prefix indicates "protected" (internal use)
- **`__`**: Double underscore prefix indicates "private" (name mangling)
- **`...`**: Ellipsis, used in protocols and abstract methods to indicate "implementation required"

### **Design Patterns Referenced**

**Builder Pattern**: Constructs complex objects step by step using a fluent interface.

**Factory Pattern**: Creates objects without specifying their exact class, often based on input parameters.

**Prototype Pattern**: Creates objects by cloning existing instances rather than creating from scratch.

**Registry Pattern**: Maintains a registry of created objects for lookup and management.

**Singleton Pattern**: Ensures only one instance of a class exists and provides global access to it.

### **Python-Specific Terms**

**`__dict__`**: A dictionary containing an object's attributes. Instance and class objects have separate `__dict__` attributes.

**`__slots__`**: A class attribute that explicitly lists allowed instance attributes, providing memory optimization.

**`hasattr()`**: Built-in function to check if an object has a specific attribute.

**`getattr()`**: Built-in function to get an attribute value with optional default.

**`setattr()`**: Built-in function to set an attribute value dynamically.

**`delattr()`**: Built-in function to delete an attribute dynamically.

**`isinstance()`**: Built-in function to check if an object is an instance of a specific type.

**`type()`**: Built-in function that returns the type of an object, or creates new types when called with three arguments.

---

This glossary covers all technical terms, concepts, and specialized vocabulary used throughout the workshop to ensure clear understanding regardless of your programming background! 📖 
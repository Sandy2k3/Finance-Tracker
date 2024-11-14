from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    user_category = models.CharField(max_length=10, choices=[
        ('business', 'Business'),
        ('personal', 'Personal'),
    ], default='personal')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


# User Categories Model
class UserCategory(models.Model):
    cat_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_categories")
    user_category = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.user.username} - {self.user_category}"


# Categories Model
class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    user_cat = models.ForeignKey(UserCategory, on_delete=models.CASCADE, related_name="categories")
    cat_name = models.CharField(max_length=150)

    def __str__(self):
        return self.cat_name


# Sub Category Model
class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="sub_categories")
    subcat_name = models.CharField(max_length=150)

    def __str__(self):
        return self.subcat_name


# Transaction Model
class Transaction(models.Model):
    t_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="transactions")
    subcat = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="transactions")
    t_description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    custom = models.CharField(max_length=255, blank=True, null=True)
    t_date = models.DateField()

    def __str__(self):
        return f"Transaction {self.t_id} - {self.amount}"

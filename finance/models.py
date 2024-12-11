from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

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
    country = models.CharField(max_length=2, choices=[
        ('AF', 'Afghanistan (AFN)'), ('AL', 'Albania (ALL)'), ('DZ', 'Algeria (DZD)'),
        ('AD', 'Andorra (EUR)'), ('AO', 'Angola (AOA)'), ('AR', 'Argentina (ARS)'),
        ('AM', 'Armenia (AMD)'), ('AU', 'Australia (AUD)'), ('AT', 'Austria (EUR)'),
        ('AZ', 'Azerbaijan (AZN)'), ('BS', 'Bahamas (BSD)'), ('BH', 'Bahrain (BHD)'),
        ('BD', 'Bangladesh (BDT)'), ('BB', 'Barbados (BBD)'), ('BY', 'Belarus (BYN)'),
        ('BE', 'Belgium (EUR)'), ('BZ', 'Belize (BZD)'), ('BJ', 'Benin (XOF)'),
        ('BT', 'Bhutan (BTN)'), ('BO', 'Bolivia (BOB)'), ('BR', 'Brazil (BRL)'),
        ('BN', 'Brunei (BND)'), ('BG', 'Bulgaria (BGN)'), ('KH', 'Cambodia (KHR)'),
        ('CM', 'Cameroon (XAF)'), ('CA', 'Canada (CAD)'), ('CL', 'Chile (CLP)'),
        ('CN', 'China (CNY)'), ('CO', 'Colombia (COP)'), ('CR', 'Costa Rica (CRC)'),
        ('HR', 'Croatia (HRK)'), ('CU', 'Cuba (CUP)'), ('CY', 'Cyprus (EUR)'),
        ('CZ', 'Czech Republic (CZK)'), ('DK', 'Denmark (DKK)'), ('DO', 'Dominican Republic (DOP)'),
        ('EC', 'Ecuador (USD)'), ('EG', 'Egypt (EGP)'), ('SV', 'El Salvador (USD)'),
        ('EE', 'Estonia (EUR)'), ('ET', 'Ethiopia (ETB)'), ('FJ', 'Fiji (FJD)'),
        ('FI', 'Finland (EUR)'), ('FR', 'France (EUR)'), ('GA', 'Gabon (XAF)'),
        ('GM', 'Gambia (GMD)'), ('GE', 'Georgia (GEL)'), ('DE', 'Germany (EUR)'),
        ('GH', 'Ghana (GHS)'), ('GR', 'Greece (EUR)'), ('GT', 'Guatemala (GTQ)'),
        ('GN', 'Guinea (GNF)'), ('HT', 'Haiti (HTG)'), ('HN', 'Honduras (HNL)'),
        ('HK', 'Hong Kong (HKD)'), ('HU', 'Hungary (HUF)'), ('IS', 'Iceland (ISK)'),
        ('IN', 'India (INR)'), ('ID', 'Indonesia (IDR)'), ('IR', 'Iran (IRR)'),
        ('IQ', 'Iraq (IQD)'), ('IE', 'Ireland (EUR)'), ('IL', 'Israel (ILS)'),
        ('IT', 'Italy (EUR)'), ('JM', 'Jamaica (JMD)'), ('JP', 'Japan (JPY)'),
        ('JO', 'Jordan (JOD)'), ('KZ', 'Kazakhstan (KZT)'), ('KE', 'Kenya (KES)'),
        ('KR', 'South Korea (KRW)'), ('KW', 'Kuwait (KWD)'), ('LB', 'Lebanon (LBP)'),
        ('LY', 'Libya (LYD)'), ('LU', 'Luxembourg (EUR)'), ('MO', 'Macau (MOP)'),
        ('MY', 'Malaysia (MYR)'), ('MV', 'Maldives (MVR)'), ('MT', 'Malta (EUR)'),
        ('MX', 'Mexico (MXN)'), ('MC', 'Monaco (EUR)'), ('MN', 'Mongolia (MNT)'),
        ('MA', 'Morocco (MAD)'), ('MZ', 'Mozambique (MZN)'), ('MM', 'Myanmar (MMK)'),
        ('NP', 'Nepal (NPR)'), ('NL', 'Netherlands (EUR)'), ('NZ', 'New Zealand (NZD)'),
        ('NG', 'Nigeria (NGN)'), ('NO', 'Norway (NOK)'), ('OM', 'Oman (OMR)'),
        ('PK', 'Pakistan (PKR)'), ('PA', 'Panama (PAB)'), ('PG', 'Papua New Guinea (PGK)'),
        ('PY', 'Paraguay (PYG)'), ('PE', 'Peru (PEN)'), ('PH', 'Philippines (PHP)'),
        ('PL', 'Poland (PLN)'), ('PT', 'Portugal (EUR)'), ('QA', 'Qatar (QAR)'),
        ('RO', 'Romania (RON)'), ('RU', 'Russia (RUB)'), ('RW', 'Rwanda (RWF)'),
        ('SA', 'Saudi Arabia (SAR)'), ('SN', 'Senegal (XOF)'), ('RS', 'Serbia (RSD)'),
        ('SG', 'Singapore (SGD)'), ('SK', 'Slovakia (EUR)'), ('SI', 'Slovenia (EUR)'),
        ('ZA', 'South Africa (ZAR)'), ('ES', 'Spain (EUR)'), ('LK', 'Sri Lanka (LKR)'),
        ('SE', 'Sweden (SEK)'), ('CH', 'Switzerland (CHF)'), ('TW', 'Taiwan (TWD)'),
        ('TZ', 'Tanzania (TZS)'), ('TH', 'Thailand (THB)'), ('TN', 'Tunisia (TND)'),
        ('TR', 'Turkey (TRY)'), ('UG', 'Uganda (UGX)'), ('UA', 'Ukraine (UAH)'),
        ('AE', 'United Arab Emirates (AED)'), ('GB', 'United Kingdom (GBP)'),
        ('US', 'United States (USD)'), ('UY', 'Uruguay (UYU)'), ('VE', 'Venezuela (VES)'),
        ('VN', 'Vietnam (VND)'), ('YE', 'Yemen (YER)'), ('ZM', 'Zambia (ZMW)'),
        ('ZW', 'Zimbabwe (ZWL)')
    ], default='US')
    is_active = models.BooleanField(default=True)

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

    # New fields for descriptive labels
    category_name = models.CharField(max_length=255, default='Default Category')

    subcategory_name = models.CharField(max_length=150, default='Default SubCategory')

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if this is a new transaction
        
        # Populate category and subcategory names
        self.category_name = self.subcat.category.cat_name
        self.subcategory_name = self.subcat.subcat_name
        
        super().save(*args, **kwargs)
        
        # Update bank balance only for new transactions
        if is_new:
            bank_balance = self.user.bank_balance
            bank_balance.update_balance(self.amount, self.category_name)

    def __str__(self):
        return f"Transaction {self.t_id} - {self.amount}"

    class Meta:
        ordering = ['-t_date', '-t_id']  # Most recent first

class BankBalance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='bank_balance')
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Balance: {self.balance}"

    def update_balance(self, transaction_amount, transaction_type):
        if transaction_type == 'Income':
            self.balance += transaction_amount
        else:  # Expenses
            self.balance -= transaction_amount
        self.save()
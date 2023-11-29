from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db.models import CASCADE, Model, TextField, ForeignKey, EmailField, CharField, SlugField, DateTimeField, \
    ManyToManyField, BooleanField, IntegerField, TextChoices, ImageField
from django.utils.text import slugify
from django_resized import ResizedImageField


class Category(Model):
    name = CharField(max_length=255)
    image = ResizedImageField(upload_to='category/')
    slug = SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        while Category.objects.filter(slug=self.slug).exists():
            slug = Category.objects.filter(slug=self.slug).first().slug
            if '-' in slug:
                try:
                    if slug.split('-')[-1] in self.name:
                        self.slug += '-1'
                    else:
                        self.slug = '-'.join(slug.split('-')[:-1]) + '-' + str(int(slug.split('-')[-1]) + 1)
                except:
                    self.slug = slug + '-1'
            else:
                self.slug += '-1'

        super().save(*args, **kwargs)


class User(AbstractUser):
    # name = CharField(max_length=255)
    email = EmailField(max_length=300)
    phone = CharField(max_length=200)
    bio = TextField(null=True, blank=True)
    image = ImageField(upload_to='user/', default='profile/user.png')
    # password = CharField(max_length=400)
    is_active = BooleanField(default=False)

    class Meta:
        verbose_name = 'Users'

    def __str__(self):
        return self.username


class Blog(Model):
    class Status(TextChoices):
        PENDING = 'pending', 'Pending'
        ACTIVE = 'active', 'Active'
        CANCEL = 'cancel', 'Cancel'
    title = CharField(max_length=300)
    description = RichTextField()
    image = ResizedImageField(upload_to='blogs/%m')
    user = ForeignKey(User, CASCADE, null=False)
    category = ManyToManyField(Category)
    view = IntegerField(default=0)
    status = CharField(max_length=25, choices=Status.choices, default=Status.PENDING)
    created_at = DateTimeField(auto_now=True)
    slug = SlugField(max_length=300, unique=True)

    class Meta:
        db_table = 'blog'
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        while Category.objects.filter(slug=self.slug).exists():
            slug = Category.objects.filter(slug=self.slug).first().slug
            if '-' in slug:
                try:
                    if slug.split('-')[-1] in self.title:
                        self.slug += '-1'
                    else:
                        self.slug = '-'.join(slug.split('-')[:-1]) + '-' + str(int(slug.split('-')[-1]) + 1)
                except:
                    self.slug = slug + '-1'
            else:
                self.slug += '-1'

        super().save(*args, **kwargs)


class Comment(Model):
    text = TextField()
    user = ForeignKey(User, CASCADE, null=False)
    blog = ForeignKey(Blog, CASCADE, related_name='blog_comment')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text


class AboutUs(Model):
    about = TextField()
    phone = CharField(max_length=50)
    address = CharField(max_length=300)
    email = EmailField(max_length=300)

    class Meta:
        verbose_name = 'AboutUs'
        verbose_name_plural = 'AboutUs'


class ContactMessage(Model):
    name = CharField(max_length=100)
    email = EmailField()
    website = CharField(max_length=100, blank=True, null=True)
    message = TextField()

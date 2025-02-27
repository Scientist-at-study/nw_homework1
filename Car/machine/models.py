from django.db import models

# Create your models here.


class Brand(models.Model):
    title = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="brand/icons", null=True, blank=True)
    created_at = models.DateField()

    def __str__(self):
        return self.title


class Color(models.Model):
    color = models.CharField(max_length=7, default='#FFFFFF')

    def __str__(self):
        return self.color


class Car(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Brand")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name="Color")
    price = models.PositiveIntegerField(verbose_name="Car price")
    photo = models.ImageField(upload_to="car/photos", null=True, blank=True, verbose_name="Photo")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Machines"
        verbose_name = "Machine"


class Comment(models.Model):
    car = models.ForeignKey("Car", on_delete=models.CASCADE, related_name="comments")
    author = models.CharField(max_length=100, verbose_name="Author")
    comment = models.TextField(verbose_name="Comment by author")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.car}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]

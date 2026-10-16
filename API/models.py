from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# uuid
class Meal(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)

    @property
    def no_of_ratings(self):
        return Rating.objects.filter(meal=self).count()

    @property
    def avg_rating(self):
        ratings = Rating.objects.filter(meal=self)
        total = sum(rating.stars for rating in ratings)
        count = ratings.count()

        if count > 0:
            return total / count
        return 0
def __str__(self):
        return self.title

class Rating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

class Meta:
    constraints = [ models.UniqueConstraint(
            fields=['user', 'meal'],
            name='unique_user_meal_rating'
        )
    ]


        
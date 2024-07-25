from django.db import models
from django.utils.timezone import now as timezone_now


# Create your models here.
class CreationModificationDateMixin(models.Model):
    created = models.DateTimeField("创建时间", editable=False)
    modified = models.DateTimeField("修改时间", editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = timezone_now()
        else:
            if not self.created:
                self.created = timezone_now()
        self.modified = timezone_now()
        super(CreationModificationDateMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class BayesResult(CreationModificationDateMixin):
    vocab = models.TextField('词汇表')
    p1V = models.TextField('p1V')
    p0V = models.TextField('p0V')
    PAb = models.FloatField("P(A|B)")

    class Meta:
        verbose_name = '贝叶斯情感分析'
        verbose_name_plural = '贝叶斯情感分析'

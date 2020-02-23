from django.db import models
from seval import safe_eval

from credo_classification.drf import DjangoPlusViewPermissionsMixin
from users.models import User


class Attribute(models.Model):
    """
    Attribute definition for cosmic-ray hits. It is simple RDF based semantic net attribute.

    All attributes store float64 value (15+ significant digits).
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='', blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return 'Attribute: %s' % self.name

    class Meta(DjangoPlusViewPermissionsMixin):
        pass


class Relation(models.Model):
    """
    Semantic net relation between attributes.

    Weight of relation is evaluated by arithmetic function executed by seval library. I.e.:
    evaluation='x * 2', where x was replaced by src attribute value
    """
    name = models.CharField(max_length=255)
    description = models.TextField(default='', blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    src = models.ForeignKey(Attribute, on_delete=models.PROTECT, related_name='relation_src')
    dest = models.ForeignKey(Attribute, on_delete=models.PROTECT, related_name='relation_dest')
    evaluation = models.CharField(max_length=255, default='x')

    def evaluate_weight(self, src_value: float) -> float:
        """
        Evaluate weight of relation.

        :param src_value: float-value of source attribute
        :return: evaluated weight of relation
        """
        return float(safe_eval(self.evaluation.replace('x', str(src_value))))

    def __str__(self) -> str:
        return 'Attribute: %s' % self.name

    class Meta(DjangoPlusViewPermissionsMixin):
        unique_together = [['src', 'dest']]

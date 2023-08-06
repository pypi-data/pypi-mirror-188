# django-nestedquery
Given a django model such as 

```python
class SensorReading(models.Model):
    sensor=models.PositiveIntegerField()
    timestamp=models.DatetimeField()
    reading=models.IntegerField()
```

This allows the construction of queries such as 

```python
from nestedquery import NestedQuery

qs=NestedQuery(SensorReading.objects.filter(sensor=1)).filter(reading__gte=10)
```

resulting in  SQL looking something like

```SQL
SELECT * FROM (
    SELECT * FROM SensorReading
    WHERE sensor = 1
) as VirtualTable
WHERE VirtualTable.reading >= 10;
```

While this example is obviously simplistic, This Pattern becomes more useful when dealing with more complex queries, for example when dealing with aggregates

```python
readings = (
    NestedQuery(
        SensorReading.objects.filter(**filters)
        .annotate(
            previous_read=Window(
                expression=window.Lead("timestamp"),
                partition_by=[F("sensor"),],
                order_by=[
                    "timestamp",
                ],
                frame=RowRange(start=-1, end=0),
            )
        )
        .annotate(delta=Abs(Extract(F("timestamp") - F("previous_read"), "epoch")))
    )
    .values("sensor")
    .annotate(min=Min("delta"), max=Max("delta"))
)
```

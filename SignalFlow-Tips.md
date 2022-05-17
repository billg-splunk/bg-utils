# SignalFlow Tips

## Add a plot that is 1 during weekdays and 0 during weekends

This can be useful, combined with other metrics, to only show values during certain days of the week, or even specific hours of each day.

```
A = const(1).sum(cycle="week", cycle_start="sunday", partial_values=True).publish(label='A')
B = when(A > 23 and A < 144).publish(label='B')
```
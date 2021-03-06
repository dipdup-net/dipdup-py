# Scheduler configuration

DipDup utilizes `apscheduler` library to run hooks according to schedules in `jobs` config section. In the following example, `apscheduler` will spawn up to three instances of the same job every time the trigger is fired, even if previous runs are in progress:

```yaml
advanced:
  scheduler:
    apscheduler.job_defaults.coalesce: True
    apscheduler.job_defaults.max_instances: 3
```

See [`apscheduler` docs](https://apscheduler.readthedocs.io/en/stable/userguide.html#configuring-the-scheduler) for details.

Note that you can't use executors from `apscheduler.executors.pool` module - `ConfigurationError` exception will be raised.

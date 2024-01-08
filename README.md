# `tap-clinicaltrials`

Singer tap for [ClinicalTrials.gov](https://clinicaltrials.gov/data-about-studies/learn-about-api) study records data.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`

## Settings

| Setting             | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| start_date          | False    | None    | Earliest datetime to get data from |
| condition           | False    | None    | Conditions or disease query |
| sponsor             | False    | None    | Sponsor query |
| stream_maps         | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config   | False    | None    | User-defined config values to be used within map expressions. |
| flattening_enabled  | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth| False    | None    | The max depth to flatten schemas. |
| batch_config        | False    | None    |             |

A full list of supported settings and capabilities is available by running: `tap-clinicaltrials --about`

## Usage

You can easily run `tap-clinicaltrials` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-clinicaltrials --version
tap-clinicaltrials --help
tap-clinicaltrials --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install hatch
```

### Create and Run Tests

Run integration tests:

```bash
hatch run tests:integration
```

You can also test the `tap-tap-clinicaltrials` CLI interface directly:

```bash
hatch run sync:console -- --about --format=json
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Go ahead and [install Meltano](https://docs.meltano.com/getting-started/installation/) if you haven't already.

1. Install all plugins

   ```bash
   meltano install
   ```

2. Check that the extractor is working properly

   ```bash
   meltano invoke tap-tap-clinicaltrials --version
   ```

3. Execute an ELT pipeline

   ```bash
   meltano run tap-tap-clinicaltrials target-jsonl
   ```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.

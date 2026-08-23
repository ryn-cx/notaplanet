# NotAPlanet

Pluto TV API wrapper.

```python
from notaplanet import NotAPlanet

client = NotAPlanet()

results = client.search("Gunsmoke")
series_id = results.data[0].id

item = client.items([series_id]).root[0]
print(item.name, item.seasons_numbers)

for season in client.seasons(series_id).seasons:
    for episode in season.episodes:
        print(season.number, episode.number, episode.name)

for category in client.categories().categories:
    print(category.name, category.total_items_count)
```

Every endpoint is callable, and `download` and `load` are the two halves of the
call: `client.seasons.download(series_id)` returns the body as it was served and
`client.seasons.load(data)` reads it into its model.

The models are generated from the responses recorded under `tests/_files`, so
run `uv run python -m tests.generate_models` after recording a new one.

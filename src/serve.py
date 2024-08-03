from prefect import serve

from flows.stars import github_stars

# see also https://docs.prefect.io/latest/concepts/flows/#serving-multiple-flows-at-once
if __name__ == "__main__":
    serve(
        github_stars.to_deployment(
            name="Github Stars",
            tags=["test"],
            parameters={"repos": ["PrefectHQ/prefect"]},
            interval=10,
        ),
        pause_on_shutdown=False,
    )

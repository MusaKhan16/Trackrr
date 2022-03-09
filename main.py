from dataclasses import asdict
import json
import trackrr


def main():
    track = trackrr.Trail(
        elevation=100,
        difficulty=trackrr.TrackDifficulties.BLUE_SQUARE,
        sections=[trackrr.Path(100, 20, trackrr.TerrainType.GRAVEL)],
    )

    print(json.dumps(asdict(track)))


if __name__ == "__main__":
    main()

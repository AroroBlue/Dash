import time
import asterix


def decode_cat048(data, source_name):

    decoded_targets = []

    try:

        parsed = asterix.parse(data)

        for block in parsed:

            category = block.get("category")

            # Only CAT048
            if category != 48:
                continue

            records = block.get("records", [])

            for record in records:

                lat = record.get("latitude")
                lon = record.get("longitude")

                if lat is None or lon is None:
                    continue

                target = {

                    "track_number":
                        record.get("track_number", "Unknown"),

                    "callsign":
                        record.get("callsign", "Unknown"),

                    "icao":
                        record.get("target_address", "Unknown"),

                    "lat": lat,
                    "lon": lon,

                    "altitude":
                        record.get("flight_level", 0),

                    "speed":
                        record.get("ground_speed", 0),

                    "heading":
                        record.get("track_angle", 0),

                    "source":
                        source_name,

                    "timestamp":
                        time.time()
                }

                decoded_targets.append(target)

    except Exception as e:
        print(f"Decode error ({source_name}): {e}")

    return decoded_targets
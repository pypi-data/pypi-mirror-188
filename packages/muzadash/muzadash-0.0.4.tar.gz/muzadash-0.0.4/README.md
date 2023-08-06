# latest Dashboard Monitoring
This package will get the lates Dashboard Monitoring Indonesia

## How it Works?
This package will scrape Dashboard monitoring

This package will use Baoutifulsoup4 and Requests, to produce output in the form of JSON that is ready to be used in web or mobile aplications.

## How to use Lastes Qarthquake BMKG Indonesia
```commandline
if __name__ == "__main__":
    print("Aplikasi utama")
    result = gempa_terkini_BMKG.ekstraski_data()
    gempa_terkini_BMKG.tampilkan_data(result)
```
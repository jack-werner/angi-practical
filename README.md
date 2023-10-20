# angi-practical

This repositiory is Jack Werner's submission for Angi's practical coding interview. I will be using Scrapy to scrape all the roofing contractors in Macon, GA

# Setup your environment

To use this repo, first clone it and then install the dependencies using

```
pip install -r requirements.txt
```

# Running The Scraper

After you have the requirements installed you can run the scraper by first
navigating to the `bbb_contractors` directory using `cd bbb_contractors` run the command

```
scrapy crawl roofing -O ../outputs/roofing_contractors.csv
```

to output the results to a csv. (use -o if you want to append instead of overwrite)

# Get Rankings For the Contractors

After you have finished scraping the contractors, we need to rank them based on how attrictive they are as leads.
To do this, navigate back to the root of the project and run the `rank_data.py` script with the following command

```
python rank_data.py -i outputs/roofing_contractors.csv -o ranked_roofing_contractors.csv
```

`-i` is the input file and `-o` is the output file.

## Ranking explanation

The ranking for the contractors is based off of the following data, in order of most important to least important:
- BBB Rating
- Average Customer Star Rating
- Days as Accredited Business
- Days operating
- Number of complaints in the last 12 months
- Number of complaints in the last 12 years

All of the data is first min-max scaled so that the scale of the fields doesn't drastically impact the ranking. Then they are summed with linearly decreasing weights in order of importance. The complaints fields detract from the score, all others add to it. 

The thinking is that we only want to recommend good contractors to our users, because if we recommend a bad contractor, they will associate that negative experience with Angi as well. We want to prioritize the contractors that are most likely to provide good services so we don't waste our sales forces' efforts. The BBB rating and customer reviews are the most likely to reflect the quality of their services so they have the highest rank. The longer a company has been accredited, the more likely they provide quality services, and same for time operating. The number of complaints indicates negative experience but I gave these fields the lowest ranking since most companies didn't have data for this. 
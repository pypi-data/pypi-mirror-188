# README

**Goldendoodle** is a universal spider for analyzing wether domains include a search string.

It is made for a first analyze of a unknown site. The analyze one search string is done for one search string on a list of start URLs. The allowed domain(s) are extracted from the starting URLs.

The result is a Scrapy output file with Goldendoodle items.

## How to execute:
From goldendoodle run:

```bash
scrapy crawl recherchedechaîne_gldnddl -O <file> [-a gldnddlSearchString=<string>] -a option=<None|regex|email> -a start_urls=<url>[,<url>]
```
p. e.:
```bash
scrapy crawl recherchedechaîne_gldnddl -O ../reports/findings.json -a gldnddlSearchString='(Bereich.*obe[nr].*?)(?=<)' -a start_urls=https://www.drta-archiv.de/blauaugenkaerpflinge/ 2> ../reports/stderr.log
```

### option
option is optional, which means **None**. 

If gldnddlSearchString is a regular expression, than you should set option=**regex**. Otherwise findingElements and findingElementsQuery will not be filled. With option=regex you will get findingElements and findingElementsQuery only for the first finding in the site.

With option=**email** no **gldnddlSearchString** is necessary. There is a search algorithm that gives a result for the most common types of email coding. If you find an email that is not recognized, please let me know so I can adjust the algorithm.

With option=**email AND gldnddlSearchString** set, the gldnddlSearchString is used, but the results are prepared, as if emails have been searched.  

### example:

```bash
scrapy crawl recherchedechaîne_gldnddl -O reports/findings.json -a gldnddlSearchString='for use in illustrative examples in documents' -a start_urls=https://example.com/ | tee reports/log.txt
```

## Prerequisites

- see requirements.txt

## Documentation

see [Goldendoodle docs](https://melchiorim3tal.gitlab.io/goldendoodle/index.html)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
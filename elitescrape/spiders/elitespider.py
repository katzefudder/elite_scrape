import scrapy, re
import yaml
from scrapy.http.request import Request

class EliteSpider(scrapy.Spider):
  name = ""
  league_key = ''
  teams_file = ""

  teams = {}
  results = {}

  def __init__(self):
    with open(self.teams_file, 'r') as yaml_in:
      try:
          teams = yaml.load(yaml_in, Loader=yaml.FullLoader)
          self.teams = teams[self.league_key]
      except yaml.YAMLError as yamlException:
        raise yamlException

  # override start_request to use an own dict instead of start_urls
  def start_requests(self):
    for key, url in self.teams.items():
      yield Request(url, self.parse)

  def parse(self, response):
    # invert the dict
    team_keys = dict(zip(self.teams.values(), self.teams.keys()))

    # get the team's name
    team = str(response.xpath('//h1/text()').get()).strip()

    # select coach
    headCoach = response.xpath("//text()[contains(., 'Head Coach')]/following::a[1]/text()").extract()
    # select assistant coach
    assistantCoach = response.xpath("//text()[contains(., 'Assistant Coach')]/following::a[1]/text()").extract()

    # set a title
    content = "- " + str(team) + " -\n\n"

    current_team_key = ""

    # for players in response.css('table.roster tbody tr'):
    # for players in response.xpath('//table[contains(@class, "SortTable_table__")]/tbody/tr/td/div[contains(@class, "Roster_player__")]'):
    for players in response.xpath('//div[contains(@class, "Roster_player__")]'):
      
      current_team_key = team_keys[response.url]
      number = str(players.xpath('ancestor::tr/td[2]/text()').get()).strip()
      number = number.replace('#', '')

      name = str(players.xpath('a/text()').get()).strip()
      # remove any hints on the player's name
      name = str(re.sub('\(.*\)', '', name)).strip()
      if number != 'None' and name != 'None':
        content += "%s%s\t-%s- %s (%s)\n" % (current_team_key, number, number, name, team)

    if headCoach:
      content += "%s100\t%s (Trainer %s)\n" % (current_team_key, headCoach[0].strip(), team)
    if assistantCoach:
      content += "%s101\t%s (Co-Trainer %s)\n" % (current_team_key, assistantCoach[0].strip(), team)

    content += "\n\n"
    self.results[team_keys[response.url]] = content

  def __del__(self):
    content = ""
    for key in sorted(self.results):
      content += self.results[key]

    with open(self.league_key + '.txt', 'w+') as f:
      f.write(content)

from elitescrape.spiders.elitespider import EliteSpider

class StripesSpider(EliteSpider):
  name = "elite_stripes"
  league_key = 'team_stripes'
  teams_file = "teams/team_stripes.yaml"

  def __init__(self):
    super(StripesSpider, self).__init__()

  def parse(self, response):
    # invert the dict
    team_keys = dict(zip(self.teams.values(), self.teams.keys()))

    # get the team's name
    team = str(response.css('#wrapper_border #subcontent h1::text').get()).strip()

    # set a title
    content = "- " + str(team) + " -\n\n"

    for players in response.xpath('//*[@id="tabelle"]//tbody/tr'):
      current_team_key = team_keys[response.url]
      
      number = players.xpath('td[1]//text()').get().strip()
      prename = players.xpath('td[4]//text()').get().strip()
      name = players.xpath('td[3]//b//text()').get().strip()
      content += "%s%s\t-%s- %s %s (%s)\n" % (current_team_key, number, number, prename, name, team)

    self.results[team_keys[response.url]] = content
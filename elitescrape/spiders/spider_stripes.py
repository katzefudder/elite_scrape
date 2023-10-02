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
    team = str(response.xpath('//*[@id="ip_page_wrapper"]//div//section//div//div//h1//text()').get()).strip()

    # set a title
    content = "- " + str(team) + " -\n\n"

    for referees in response.xpath('//*[@id="ip_page_wrapper"]//div//section[2]//div[2]//div[@class="col"]'):
      current_team_key = team_keys[response.url]
      
      number = referees.xpath('div//div[2]/span//text()').get().strip().replace('#', '')
      prename = referees.xpath('div//div[2]/h3//text()').get().strip()
      name = referees.xpath('div//div[2]/h3//b//text()').get().strip()
      content += "%s%s\t-%s- %s %s (Hauptschiedsrichter %s)\n" % (current_team_key, number, number, prename, name, team)

    for referees in response.xpath('//*[@id="ip_page_wrapper"]//div//section[3]//div[2]//div[@class="col"]'):
      current_team_key = team_keys[response.url]
      
      number = referees.xpath('div//div[2]/span//text()').get().strip().replace('#', '')
      prename = referees.xpath('div//div[2]/h3//text()').get().strip()
      name = referees.xpath('div//div[2]/h3//b//text()').get().strip()
      content += "%s%s\t-%s- %s %s (Linesperson %s)\n" % (current_team_key, number, number, prename, name, team)

    self.results[team_keys[response.url]] = content
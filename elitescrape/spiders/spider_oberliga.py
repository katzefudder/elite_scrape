from elitescrape.spiders.elitespider import EliteSpider

class Del2Spider(EliteSpider):
  name = "elite_oberliga"
  league_key = 'oberliga'
  teams_file = "teams/oberliga.yaml"

  def __init__(self):
    super(Del2Spider, self).__init__()
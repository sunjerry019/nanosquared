speed = {
	"jog": 0,
	"min": 0,
	"max": 0
} 
self.speed    = namedtuple("StageSpeed", speed.keys())(*speed.values())
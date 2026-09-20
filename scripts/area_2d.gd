extends Area2D

var cooldown := 0.0

func _process(delta):
	if cooldown > 0:
		cooldown -= delta
		return

	for body in get_overlapping_bodies():
		if body is CharacterBody2D:
			if body.health > 0:
				body.take_damage(5)

			cooldown = 1.0
			break

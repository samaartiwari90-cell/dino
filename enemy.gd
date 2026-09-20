extends CharacterBody2D

@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D

var is_triggered: bool = false

func _ready() -> void:
	# Plays default animation on start
	animated_sprite.play("default")

# Connected Signal: Hitbox (Area2D) -> body_entered
func _on_hitbox_body_entered(body: Node2D) -> void:
	# Ignore non-player objects or if already triggered
	if not body.is_in_group("player") or is_triggered:
		return

	is_triggered = true

	# 1. Freeze player movement
	if body.has_method("die"):
		body.die()

	# 2. Play hurt animation
	if animated_sprite.sprite_frames.has_animation("hurt"):
		animated_sprite.play("hurt")
		await animated_sprite.animation_finished
	else:
		push_warning("Animation 'hurt' not found on AnimatedSprite2D!")

	# 3. Reset level
	get_tree().reload_current_scene()

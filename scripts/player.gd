extends CharacterBody2D

const JUMP_VELOCITY = -400.0

func _physics_process(delta):
	if not is_on_floor():
		velocity += get_gravity() * delta

	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	velocity.x = 0

	move_and_slide()

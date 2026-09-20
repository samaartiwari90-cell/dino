extends CharacterBody2D

const SPEED = 400.0
const JUMP_VELOCITY = -400.0

var is_dead: bool = false

func _ready() -> void:
	# Automatically adds the player to the "player" group on startup
	add_to_group("player")

func _physics_process(delta: float) -> void:
	# Lock movement and physics while dead
	if is_dead:
		return

	# Apply gravity
	if not is_on_floor():
		velocity += get_gravity() * delta

	# Handle jump input
	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	# Handle horizontal movement
	var direction := Input.get_axis("ui_left", "ui_right")
	if direction:
		velocity.x = direction * SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)

	move_and_slide()

# Called by the trap/hazard script upon collision
func die() -> void:
	if is_dead:
		return
		
	is_dead = true
	velocity = Vector2.ZERO # Instantly freeze momentum

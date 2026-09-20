extends CharacterBody2D

const SPEED = 300.0
const JUMP_VELOCITY = -400.0

var health: int = 5
var is_dead: bool = false
var invincible: bool = false
var respawn_position: Vector2

@onready var health_label: Label = $Camera2D/Label2


func _ready() -> void:
	add_to_group("player")
	respawn_position = global_position
	update_health_label()


func _physics_process(delta: float) -> void:
	if is_dead:
		return

	if not is_on_floor():
		velocity += get_gravity() * delta

	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	var direction := Input.get_axis("ui_left", "ui_right")

	if direction:
		velocity.x = direction * SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)

	move_and_slide()


func update_health_label() -> void:
	var hearts := ""

	for i in range(health):
		hearts += "♥ "

	health_label.text = hearts


func take_damage(amount: int) -> void:
	if is_dead or invincible:
		return

	health -= amount

	if health <= 0:
		health = 0
		update_health_label()
		die()
	else:
		update_health_label()
		print("DAMAGE! Health:", health)


func die() -> void:
	is_dead = true
	velocity = Vector2.ZERO

	await get_tree().create_timer(1.0).timeout

	global_position = respawn_position
	health = 5
	update_health_label()

	is_dead = false
	invincible = true
	velocity = Vector2.ZERO

	await get_tree().create_timer(2.0).timeout

	invincible = false

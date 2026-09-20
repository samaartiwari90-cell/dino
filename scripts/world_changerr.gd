extends Area2D

func _on_world_changerr_body_entered(body):
	if body is CharacterBody2D:
		get_tree().change_scene_to_file("res://world_2.tscn")

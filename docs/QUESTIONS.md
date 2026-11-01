# Evaluation Questions

Questions are written the way a Godot gameplay programmer would type them.
At least 3 need more than one file to answer, and 1 cannot be answered from my documents.

| # | Question | Where the answer is (document, page) | Needs more than one page? |
|---|---|---|---|
| 1 | How does a Node's _process callback get called each frame? | node.cpp, node.h, scene_tree.cpp, Node.xml | yes |
| 2 | Where are signals connected and emitted in the core code? | object.cpp, object.h, node.cpp, scene_tree.cpp | yes |
|| 3 | Which file implements the 2D physics body collision response? | godot_body_pair_2d.cpp | no |
| 4 | Where is the main loop iteration implemented in Godot? | main.cpp, scene_tree.cpp | yes |
| 5 | How does the SceneTree manage node groups? | scene_tree.cpp, scene_tree.h, node.cpp | yes |
| 6 | Where is the GDScript parser implemented? | gdscript_parser.cpp, gdscript_parser.h | no |
| 7 | How does the RenderingServer separate rendering from scene nodes? | rendering_server.h, rendering_server.cpp, canvas_item.cpp, node.cpp | yes |
| 8 | How are input events dispatched to _input and _unhandled_input? | viewport.cpp, node.cpp, scene_tree.cpp | yes |
| 9 | How does ResourceLoader load a .tscn scene file? | resource_loader.cpp, resource_loader.h, packed_scene.cpp | yes |
| 10 | How much does a Godot console export license cost? | (cannot be answered from my documents) | none |

# Game Architecture
## Menu Navigation

```mermaid

stateDiagram
    [*] --> Menu
    Menu --> Settings: sel
    Settings --> Menu : back
    Menu --> Game : sel
    GameN --> Pause : pause
    Pause --> Game : unpause
    Pause --> Menu : back
    Menu --> [*] : exit
    Pause --> [*] : exit

```

## Classes

```mermaid

classDiagram
    class Game {
        -current_scene
        -settings
        +run()
    }

    class Settings {
        +resolution
        +is_fullscreen
    }

    class Scene {
        <<abstract>>
        +tick()
        -handle_events(events)
        -handle_inputs()
        -update(dt)
        -draw()
    }
    
    class MenuScene{
        
    }
    class GameScene{

    }
    class SettingsScene{

    }

    Game --> Scene : current_scene
    Scene --> Game : ref
    Scene <|-- MenuScene
    Scene <|-- GameScene
    Scene <|-- SettingsScene
    Game --> Settings : settings

```

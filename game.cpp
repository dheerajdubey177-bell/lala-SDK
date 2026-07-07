#include "raylib.h"

int main(void)
{
    // Initialization
    const int screenWidth = 800;
    const int screenHeight = 450;
    
    InitWindow(screenWidth, screenHeight, "Lala SDK C++ Test - Bouncing Ball");

    Vector2 ballPosition = { (float)screenWidth/2, (float)screenHeight/2 };
    Vector2 ballSpeed = { 5.0f, 4.0f };
    int ballRadius = 20;

    SetTargetFPS(60);

    // Main game loop
    while (!WindowShouldClose())    // Detect window close button or ESC key
    {
        // Update
        ballPosition.x += ballSpeed.x;
        ballPosition.y += ballSpeed.y;

        // Check walls collision for bouncing
        if ((ballPosition.x >= (screenWidth - ballRadius)) || (ballPosition.x <= ballRadius)) ballSpeed.x *= -1.0f;
        if ((ballPosition.y >= (screenHeight - ballRadius)) || (ballPosition.y <= ballRadius)) ballSpeed.y *= -1.0f;

        // Draw
        BeginDrawing();
            ClearBackground(RAYWHITE);
            
            DrawText("Lala C++ Compiler Test", 10, 10, 20, DARKGRAY);
            DrawText("This simulates the C++ transpilation output!", 10, 40, 20, GRAY);
            
            DrawCircleV(ballPosition, (float)ballRadius, MAROON);
        EndDrawing();
    }

    // De-Initialization
    CloseWindow();

    return 0;
}

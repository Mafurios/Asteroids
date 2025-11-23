import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_SHOOT_SPEED, PLAYER_TURN_SPEED, PLAYER_SPEED, SHOT_RADIUS, PLAYER_SHOOT_COOLDOWN_SECONDS
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        radius = PLAYER_RADIUS
        super().__init__(x, y, radius)
        self.rotation = 0
        self.shoot_cooldown_timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if not self.shoot_cooldown_timer > 0:
                self.shoot()
                self.shoot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        shot = Shot(self.position[0], self.position[1], SHOT_RADIUS)
        shot_vector = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = shot_vector * PLAYER_SHOOT_SPEED * 0.3

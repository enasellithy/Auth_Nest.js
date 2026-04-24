Phase 1: Foundation - RESTful API with JWT Authentication (NestJS)

🎯 Description:
The goal of this milestone is to establish a secure, scalable RESTful API using the NestJS framework. This includes setting up the core architecture, database integration (PostgreSQL/MongoDB), and a robust authentication system using JSON Web Tokens (JWT).

🛠️ Included Tasks (Issues):
1. Project Initialization & Structure
Generate a new NestJS project using the CLI.

Setup environment variables configuration (.env) for database credentials and JWT secrets.

Implement a global exception filter and response interceptor for consistent API outputs.

2. User Module & Database Integration
Create a User entity/schema with fields: id, email, password, and role.

Implement a UsersService to handle user creation and lookup.

Integrate TypeORM or Mongoose for database connectivity.

3. Authentication System (JWT)
Implement AuthModule using @nestjs/jwt and @nestjs/passport.

Create a Sign-up endpoint with password hashing (using bcrypt).

Create a Login endpoint that returns a signed JWT access token.

4. Security Guards & Protected Routes
Implement a JwtStrategy to validate tokens on incoming requests.

Create a custom @UseGuards(JwtAuthGuard) to protect sensitive endpoints.

Add a /me profile endpoint to test authentication and return current user data.

5. API Documentation (Swagger)
Integrate @nestjs/swagger to auto-generate API documentation.

Ensure all endpoints are properly decorated with summary and response types.

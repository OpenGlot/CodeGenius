To expand your `UserRepository` to include functionality for retrieving a user's profile along with their badges, notifications, flashcards, and progress, you will need to update both the repository interface (`IUserRepository`) and its implementation (`UserRepository`). Additionally, you will need to ensure that the necessary navigation properties are correctly configured in your `ApplicationDbContext` and model classes.

Here's how you can expand your code:

### Step 1: Update `IUserRepository` Interface

Add a new method to fetch a detailed user profile, including badges, notifications, flashcards, and progress.

```csharp
namespace PolyglotAPI.Data.Repos
{
    public interface IUserRepository
    {
        Task<IEnumerable<UserProfile>> GetAllUsersAsync();
        Task<UserProfile> GetUserByIdAsync(string userId);
        Task<UserProfile> GetDetailedUserProfileAsync(string userId);
        Task AddUserAsync(UserProfile user);
        Task UpdateUserAsync(UserProfile user);
        Task DeleteUserAsync(string userId);
        
        Task<IEnumerable<UserRole>> GetUserRolesAsync(string userId);
        Task AddUserRoleAsync(UserRole userRole);
        Task RemoveUserRoleAsync(string userId, int roleId);
    }
}
```

### Step 2: Update `UserRepository` Implementation

Implement the new method in `UserRepository`.

```csharp
using Microsoft.EntityFrameworkCore;
using PolyglotAPI.Data.Models;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Linq;

namespace PolyglotAPI.Data.Repos
{
    public class UserRepository : IUserRepository
    {
        private readonly ApplicationDbContext _context;

        public UserRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<UserProfile>> GetAllUsersAsync()
        {
            return await _context.UserProfiles.ToListAsync();
        }

        public async Task<UserProfile> GetUserByIdAsync(string userId)
        {
            return await _context.UserProfiles
                                 .Include(u => u.UserRoles)
                                 .ThenInclude(ur => ur.Role)
                                 .FirstOrDefaultAsync(u => u.UserId == userId);
        }

        public async Task<UserProfile> GetDetailedUserProfileAsync(string userId)
        {
            return await _context.UserProfiles
                                 .Include(u => u.UserRoles)
                                 .ThenInclude(ur => ur.Role)
                                 .Include(u => u.Badges)
                                 .Include(u => u.Notifications)
                                 .Include(u => u.Flashcards)
                                 .Include(u => u.Progresses)
                                 .FirstOrDefaultAsync(u => u.UserId == userId);
        }

        public async Task AddUserAsync(UserProfile user)
        {
            await _context.UserProfiles.AddAsync(user);
            await _context.SaveChangesAsync();
        }

        public async Task UpdateUserAsync(UserProfile user)
        {
            _context.UserProfiles.Update(user);
            await _context.SaveChangesAsync();
        }

        public async Task DeleteUserAsync(string userId)
        {
            var user = await _context.UserProfiles.FindAsync(userId);
            if (user != null)
            {
                _context.UserProfiles.Remove(user);
                await _context.SaveChangesAsync();
            }
        }

        public async Task<IEnumerable<UserRole>> GetUserRolesAsync(string userId)
        {
            return await _context.UserRoles
                                 .Where(ur => ur.UserId == userId)
                                 .Include(ur => ur.Role)
                                 .ToListAsync();
        }

        public async Task AddUserRoleAsync(UserRole userRole)
        {
            await _context.UserRoles.AddAsync(userRole);
            await _context.SaveChangesAsync();
        }

        public async Task RemoveUserRoleAsync(string userId, int roleId)
        {
            var userRole = await _context.UserRoles
                                         .FirstOrDefaultAsync(ur => ur.UserId == userId && ur.RoleId == roleId);
            if (userRole != null)
            {
                _context.UserRoles.Remove(userRole);
                await _context.SaveChangesAsync();
            }
        }
    }
}
```

### Step 3: Modify `ApplicationDbContext` Configuration

Ensure that your `OnModelCreating` method in `ApplicationDbContext` configuration supports the necessary relationships.

```csharp
using Microsoft.EntityFrameworkCore;
using PolyglotAPI.Data.Models;

namespace PolyglotAPI.Data
{
    public class ApplicationDbContext : DbContext
    {
        public DbSet<Language> Languages { get; set; }
        public DbSet<Course> Courses { get; set; }
        public DbSet<Module> Modules { get; set; }
        public DbSet<Lesson> Lessons { get; set; }
        public DbSet<Question> Questions { get; set; }
        public DbSet<Option> Options { get; set; }
        public DbSet<Audio> Audios { get; set; }
        public DbSet<Image> Images { get; set; }
        public DbSet<UserProfile> UserProfiles { get; set; }
        public DbSet<Role> Roles { get; set; }
        public DbSet<UserRole> UserRoles { get; set; }
        public DbSet<Rating> Ratings { get; set; }
        public DbSet<Progress> Progresses { get; set; }
        public DbSet<Badge> Badges { get; set; }
        public DbSet<Notification> Notifications { get; set; }
        public DbSet<Flashcard> Flashcards { get; set; }
        public DbSet<UserGeneratedContent> UserGeneratedContents { get; set; }
        public DbSet<Subscription> Subscriptions { get; set; }
        public DbSet<InteractiveStorybook> InteractiveStorybooks { get; set; }
        public DbSet<StoryChoice> StoryChoices { get; set; }

        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options) { }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<UserProfile>(entity =>
            {
                entity.HasKey(e => e.UserId);
                entity.HasMany(e => e.UserRoles).WithOne(e => e.User).HasForeignKey(e => e.UserId);
                entity.HasMany(e => e.Ratings).WithOne(e => e.User).HasForeignKey(e => e.UserId);
                entity.HasMany(e => e.Progresses).WithOne(e => e.User).HasForeignKey(e => e.UserId);
                entity.HasMany(e => e.Badges).WithOne(e => e.User).HasForeignKey(e => e.UserId);
                entity.HasMany(e => e.Notifications).WithOne(e => e.User).HasForeignKey(e => e.UserId);
                entity.HasMany(e => e.Flashcards).WithOne(e => e.User).HasForeignKey(e => e.UserId);
                entity.HasMany(e => e.UserGeneratedContents).WithOne(e => e.User).HasForeignKey(e => e.UserId);
                entity.HasOne(e => e.Subscription).WithOne(e => e.User).HasForeignKey<Subscription>(e => e.UserId);
            });

            modelBuilder.Entity<Role>(entity => { entity.HasKey(e => e.RoleId); });

            modelBuilder.Entity<UserRole>(entity =>
            {
                entity.HasKey(e => e.UserRoleId);
                entity.HasOne(e => e.User).WithMany(e => e.UserRoles).HasForeignKey(e => e.UserId);
                entity.HasOne(e => e.Role).WithMany().HasForeignKey(e => e.RoleId);
            });

            modelBuilder.Entity<Rating>(entity =>
            {
                entity.HasKey(e => e.RatingId);
                entity.HasOne(e => e.User).WithMany(e => e.Ratings).HasForeignKey(e => e.UserId);
                entity.HasOne(e => e.Lesson).WithMany(e => e.Ratings).HasForeignKey(e => e.ContentId);
            });

            modelBuilder.Entity<Progress>(entity =>
            {
                entity.HasKey(e => e.ProgressId);
                entity.HasOne(e => e.User).WithMany(e => e.Progresses).HasForeignKey(e => e.UserId);
                entity.HasOne(e => e.Module).WithMany(e => e.Progresses).HasForeignKey(e => e.ModuleId);
                entity.HasOne(e => e.Course).WithMany().HasForeignKey(e => e.CourseId);
            });

            // Other model configurations

            base.OnModelCreating(modelBuilder);
        }
    }
}
```

### Step 4: Use the Method in a Service or Controller

Finally, you can call this method from a service or controller where needed.

```csharp
using Microsoft.AspNetCore.Mvc;
using PolyglotAPI.Data.Repos;

[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly IUserRepository _userRepository;
    private readonly ILogger<UsersController> _logger;

    public UsersController(IUserRepository userRepository, ILogger<UsersController> logger)
    {
        _userRepository = userRepository;
        _logger = logger;
    }

    [HttpGet("{id}/profile")]
    public async Task<IActionResult> GetUserProfile(string id)
    {
        _logger.LogInformation($"Retrieving detailed profile for user ID: {id}");
        var userProfile = await _userRepository.GetDetailedUserProfileAsync(id);

        if (userProfile == null)
        {
            _logger.LogWarning($"User with ID: {id} not found");
            return NotFound();
        }

        return Ok(userProfile);
    }
}
```

This expansion allows you to fetch a user's detailed profile, enhancing the functionalities of your `UserRepository`. Ensure that all navigation properties and relationships are correctly configured within `ApplicationDbContext` to support these queries.
To expand your repository pattern and add endpoints to your `UsersController` for retrieving a user profile along with related badges, notifications, flashcards, and progress, you'll need to follow these steps:

1. **Expand the `IUserRepository` interface:**

Expand the `IUserRepository` interface to include methods for retrieving badges, notifications, flashcards, and progress for a user.

```csharp
public interface IUserRepository
{
    Task<UserProfile> GetUserProfileAsync(string userId);
    Task<IEnumerable<Badge>> GetUserBadgesAsync(string userId);
    Task<IEnumerable<Notification>> GetUserNotificationsAsync(string userId);
    Task<IEnumerable<Flashcard>> GetUserFlashcardsAsync(string userId);
    Task<IEnumerable<Progress>> GetUserProgressesAsync(string userId);
}
```

2. **Implement the expanded methods in `UserRepository`:**

Implement these methods in the `UserRepository` class.

```csharp
public class UserRepository : IUserRepository
{
    private readonly ApplicationDbContext _context;

    public UserRepository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<UserProfile> GetUserProfileAsync(string userId)
    {
        return await _context.UserProfiles
                             .Include(u => u.Badges)
                             .Include(u => u.Notifications)
                             .Include(u => u.Flashcards)
                             .Include(u => u.Progresses)
                             .FirstOrDefaultAsync(u => u.UserId == userId);
    }

    public async Task<IEnumerable<Badge>> GetUserBadgesAsync(string userId)
    {
        return await _context.Badges.Where(b => b.UserId == userId).ToListAsync();
    }

    public async Task<IEnumerable<Notification>> GetUserNotificationsAsync(string userId)
    {
        return await _context.Notifications.Where(n => n.UserId == userId).ToListAsync();
    }

    public async Task<IEnumerable<Flashcard>> GetUserFlashcardsAsync(string userId)
    {
        return await _context.Flashcards.Where(f => f.UserId == userId).ToListAsync();
    }

    public async Task<IEnumerable<Progress>> GetUserProgressesAsync(string userId)
    {
        return await _context.Progresses.Where(p => p.UserId == userId).ToListAsync();
    }
}
```

3. **Modify the `UsersController` to use the `UserRepository`:**

Add endpoints in `UsersController` to retrieve user profile, badges, notifications, flashcards, and progress using the `UserRepository`.

```csharp
[Route("api/[controller]")]
[ApiController]
public class UsersController : ControllerBase
{
    private readonly IUserRepository _userRepository;
    private readonly ILogger<UsersController> _logger;

    public UsersController(IUserRepository userRepository, ILogger<UsersController> logger)
    {
        _userRepository = userRepository;
        _logger = logger;
    }

    // GET: api/Users/{id}/Profile
    [HttpGet("{id}/Profile")]
    public async Task<ActionResult<UserProfile>> GetUserProfile(string id)
    {
        _logger.LogInformation($"Getting profile for user with ID: {id}");
        var userProfile = await _userRepository.GetUserProfileAsync(id);
        if (userProfile == null)
        {
            return NotFound();
        }
        return Ok(userProfile);
    }

    // GET: api/Users/{id}/Badges
    [HttpGet("{id}/Badges")]
    public async Task<ActionResult<IEnumerable<Badge>>> GetUserBadges(string id)
    {
        _logger.LogInformation($"Getting badges for user with ID: {id}");
        var badges = await _userRepository.GetUserBadgesAsync(id);
        return Ok(badges);
    }

    // GET: api/Users/{id}/Notifications
    [HttpGet("{id}/Notifications")]
    public async Task<ActionResult<IEnumerable<Notification>>> GetUserNotifications(string id)
    {
        _logger.LogInformation($"Getting notifications for user with ID: {id}");
        var notifications = await _userRepository.GetUserNotificationsAsync(id);
        return Ok(notifications);
    }

    // GET: api/Users/{id}/Flashcards
    [HttpGet("{id}/Flashcards")]
    public async Task<ActionResult<IEnumerable<Flashcard>>> GetUserFlashcards(string id)
    {
        _logger.LogInformation($"Getting flashcards for user with ID: {id}");
        var flashcards = await _userRepository.GetUserFlashcardsAsync(id);
        return Ok(flashcards);
    }

    // GET: api/Users/{id}/Progresses
    [HttpGet("{id}/Progresses")]
    public async Task<ActionResult<IEnumerable<Progress>>> GetUserProgresses(string id)
    {
        _logger.LogInformation($"Getting progresses for user with ID: {id}");
        var progresses = await _userRepository.GetUserProgressesAsync(id);
        return Ok(progresses);
    }
}
```

4. **Verify Dependency Injection Configuration:**

Ensure that `IUserRepository` is properly registered in your `Startup.ConfigureServices` method.

```csharp
public void ConfigureServices(IServiceCollection services)
{
    services.AddControllers();
    
    // Add the UserRepository to the DI container
    services.AddScoped<IUserRepository, UserRepository>();

    // Other configurations...
}
```

By following these steps, you add the necessary methods to your repository and define the corresponding endpoints in your controller, enabling you to retrieve user profile details, badges, notifications, flashcards, and progress.
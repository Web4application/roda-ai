import Vapor
import Queues

public func configure(_ app: Application) throws {
// Register the scheduler
app.queues.use(.memory)

// Schedule a task to run at a specific time
app.queues.schedule(MyScheduledTask())
.daily()
.at(.midnight)
}

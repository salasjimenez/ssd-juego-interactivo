using Samurai.Core;
using Xunit;

namespace Samurai.Tests;

public sealed class ProjectDefinitionTests
{
    [Fact]
    public void Name_ShouldMatchApprovedVision()
    {
        Assert.Equal("SAMURAI", ProjectDefinition.Name);
    }

    [Fact]
    public void ApprovedScope_ShouldContainExpectedCounts()
    {
        Assert.Equal(50, ProjectDefinition.TotalStages);
        Assert.Equal(10, ProjectDefinition.AcademicCycles);
        Assert.Equal(1000, ProjectDefinition.AcademicLevels);
        Assert.Equal(16, ProjectDefinition.ProfessionalClans);
    }

    [Theory]
    [InlineData(1)]
    [InlineData(500)]
    [InlineData(1000)]
    public void AcademicLevelInRange_ShouldAcceptValidNumbers(int level)
    {
        Assert.True(ProjectDefinition.IsAcademicLevelInRange(level));
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(1001)]
    public void AcademicLevelInRange_ShouldRejectInvalidNumbers(int level)
    {
        Assert.False(ProjectDefinition.IsAcademicLevelInRange(level));
    }
}

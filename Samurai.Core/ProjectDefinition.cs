namespace Samurai.Core;

/// <summary>
/// Constantes iniciales del alcance aprobado en la Etapa 1.
/// Los modelos de Ciclo, Curso, Nivel y Progreso se implementan en la Etapa 7.
/// </summary>
public static class ProjectDefinition
{
    public const string Name = "SAMURAI";
    public const int TotalStages = 50;
    public const int AcademicCycles = 10;
    public const int AcademicLevels = 1000;
    public const int ProfessionalClans = 16;

    /// <summary>Comprueba solo el rango de un numero de nivel academico.</summary>
    public static bool IsAcademicLevelInRange(int level) =>
        level is >= 1 and <= AcademicLevels;
}

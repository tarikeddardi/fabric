CREATE TABLE [dbo].[FactLogement] (

	[LogementID] bigint NULL, 
	[TypologieID] int NULL, 
	[ConstructionID] int NULL, 
	[FinancementID] int NULL, 
	[NbLogement] int NULL
);


GO
ALTER TABLE [dbo].[FactLogement] ADD CONSTRAINT FK_2734efb4_d2be_47e1_99e3_2ed55a554923 FOREIGN KEY ([FinancementID]) REFERENCES dbo.DimFinancement([FinancementID]);
GO
ALTER TABLE [dbo].[FactLogement] ADD CONSTRAINT FK_37467c68_cf4c_49d8_90d4_624ab918bc35 FOREIGN KEY ([TypologieID]) REFERENCES dbo.DimTypologie([TypologieID]);
GO
ALTER TABLE [dbo].[FactLogement] ADD CONSTRAINT FK_abae0538_28f5_44eb_b543_2fc6affca418 FOREIGN KEY ([ConstructionID]) REFERENCES dbo.DimConstruction([ConstructionID]);
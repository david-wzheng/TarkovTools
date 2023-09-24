import { LogTextColor } from "@spt-aki/models/spt/logging/LogTextColor";

// WTT imports
import { InstanceManager } from "./InstanceManager";

export class WTTRouterService 
{
    // eslint-disable-next-line @typescript-eslint/naming-convention
    private Instance: InstanceManager;

    public preAkiLoad(instance: InstanceManager): void
    {
        this.Instance = instance;
        this.registerQuestZoneRoute();
        this.Instance.logger.log(`[${this.Instance.modName}] Initialized and registered routes.`, LogTextColor.GREEN);
    }

    private registerQuestZoneRoute(): void
    {
        this.Instance.staticRouter.registerStaticRouter(
            "GetZones",
            [
                {
                    url: "/quests/zones/getZones",
                    // eslint-disable-next-line @typescript-eslint/no-unused-vars
                    action: (url, info, sessionId, output) => 
                    {
                        const json = JSON.stringify(
                            this.Instance.database.globals["QuestZones"]
                        );
                        this.Instance.logger.log(`[${this.Instance.modName}] Zones requested by client`, LogTextColor.GREEN);
                        return json;
                    }
                }
            ],
            ""
        );
    }

    private registerFlareZoneRoute(): void
    {

    }

    private registerBotKillRoute(): void
    {

    }
}
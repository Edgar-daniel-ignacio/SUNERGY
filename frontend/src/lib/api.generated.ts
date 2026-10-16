/** Generated from contracts/openapi.json. Run npm run api:generate; do not edit. */
export interface paths {
    "/api/v1/capabilities": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Capabilities */
        get: operations["getCapabilities"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/module-iv": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Post Module Iv */
        post: operations["requestModuleIV"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/health": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Health */
        get: operations["getHealth"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
}
export type webhooks = Record<string, never>;
export interface components {
    schemas: {
        /** CapabilityResponse */
        CapabilityResponse: {
            /**
             * Calibration
             * @default not_implemented
             * @constant
             */
            calibration: "not_implemented";
            /**
             * Legacy Reproduction
             * @default missing_reference_outputs
             * @constant
             */
            legacy_reproduction: "missing_reference_outputs";
            /**
             * Measurement Comparison
             * @default not_implemented
             * @constant
             */
            measurement_comparison: "not_implemented";
            /**
             * Module Iv
             * @default not_implemented
             * @constant
             */
            module_iv: "not_implemented";
            /**
             * Scientific Verification
             * @default not_performed
             * @constant
             */
            scientific_verification: "not_performed";
        };
        /** CatalogModule */
        CatalogModule: {
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "catalog";
            source_record: components["schemas"]["SourceRecord"];
        };
        /** HTTPValidationError */
        HTTPValidationError: {
            /** Detail */
            detail?: components["schemas"]["ValidationError"][];
        };
        /** HealthResponse */
        HealthResponse: {
            /**
             * Service
             * @default sunergy
             * @constant
             */
            service: "sunergy";
            /**
             * Status
             * @default ok
             * @constant
             */
            status: "ok";
            /** Version */
            version: string;
        };
        /** ManualModule */
        ManualModule: {
            /**
             * Alpha Sc A Per C
             * @description Absolute Isc temperature coefficient, A/°C
             */
            alpha_sc_a_per_c: number;
            /**
             * Beta Voc V Per C
             * @description Absolute Voc temperature coefficient, V/°C
             */
            beta_voc_v_per_c: number;
            /**
             * Cell Type
             * @enum {string}
             */
            cell_type: "monoSi" | "multiSi" | "polySi" | "cis" | "cigs" | "cdte" | "amorphous";
            /** Cells In Series */
            cells_in_series: number;
            /**
             * Gamma Pmp Percent Per C
             * @description Pmp coefficient, percent/°C, not Vmp
             */
            gamma_pmp_percent_per_c: number;
            /** I Mp A */
            i_mp_a: number;
            /** I Sc A */
            i_sc_a: number;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "manual";
            /** Name */
            name: string;
            /** Reference Cell Temperature C */
            reference_cell_temperature_c: number;
            /** Reference Irradiance W M2 */
            reference_irradiance_w_m2: number;
            source_record?: components["schemas"]["SourceRecord"] | null;
            /** V Mp V */
            v_mp_v: number;
            /** V Oc V */
            v_oc_v: number;
        };
        /**
         * ModuleIVRequest
         * @description Reserved point-simulation boundary; no model is implemented yet.
         */
        ModuleIVRequest: {
            /**
             * Model Id
             * @description Explicit versioned selection; no production default
             */
            model_id: string;
            /** Module */
            module: components["schemas"]["ManualModule"] | components["schemas"]["CatalogModule"];
            operating_point: components["schemas"]["OperatingPoint"];
            site: components["schemas"]["Site"];
        };
        /** OperatingPoint */
        OperatingPoint: {
            /**
             * Cell Temperature C
             * @description Cell, not ambient temperature
             */
            cell_temperature_c: number;
            /**
             * Effective Irradiance W M2
             * @description Effective in-plane irradiance
             */
            effective_irradiance_w_m2: number;
        };
        /** Site */
        Site: {
            /** Latitude Deg */
            latitude_deg: number;
            /** Longitude Deg */
            longitude_deg: number;
            /**
             * Timezone
             * @description IANA zone; no inferred current UTC offset
             */
            timezone: string;
        };
        /** SourceRecord */
        SourceRecord: {
            /** Record Id */
            record_id: string;
            /** Snapshot Sha256 */
            snapshot_sha256: string;
            /** Source Id */
            source_id: string;
        };
        /** UnavailableResponse */
        UnavailableResponse: {
            /**
             * Code
             * @default module_iv_not_implemented
             * @constant
             */
            code: "module_iv_not_implemented";
            /**
             * Message
             * @default Module I–V simulation awaits independent legacy capture and implementation.
             */
            message: string;
        };
        /** ValidationError */
        ValidationError: {
            /** Context */
            ctx?: Record<string, never>;
            /** Input */
            input?: unknown;
            /** Location */
            loc: (string | number)[];
            /** Message */
            msg: string;
            /** Error Type */
            type: string;
        };
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
    getCapabilities: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["CapabilityResponse"];
                };
            };
        };
    };
    requestModuleIV: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ModuleIVRequest"];
            };
        };
        responses: {
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
            /** @description Successful Response */
            501: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["UnavailableResponse"];
                };
            };
        };
    };
    getHealth: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HealthResponse"];
                };
            };
        };
    };
}

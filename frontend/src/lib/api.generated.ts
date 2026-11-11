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
    "/api/v1/compatibility/iv-r": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Post Legacy Iv */
        post: operations["reproduceLegacyIV"];
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
        /** CalculationFailure */
        CalculationFailure: {
            /**
             * Code
             * @default legacy_iv_calculation_failed
             * @constant
             */
            code: "legacy_iv_calculation_failed";
            /**
             * Message
             * @default The compatibility fit or calculation did not return finite supported outputs.
             */
            message: string;
        };
        /** CapabilityResponse */
        CapabilityResponse: {
            /**
             * Calibration
             * @default not_implemented
             * @constant
             */
            calibration: "not_implemented";
            /** Compatibility Models */
            compatibility_models?: string[];
            /**
             * Legacy Reproduction
             * @default partial_iv_r_and_thermal
             * @constant
             */
            legacy_reproduction: "partial_iv_r_and_thermal";
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
             * @default incomplete_mpp_target_unmet
             * @constant
             */
            scientific_verification: "incomplete_mpp_target_unmet";
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
        /** LegacyIVCase */
        LegacyIVCase: {
            /** Cell Temperature C */
            cell_temperature_c: number;
            /** Comparison I Mp A */
            comparison_i_mp_a: number;
            /** Comparison I Sc A */
            comparison_i_sc_a: number;
            /**
             * Comparison P Mp W
             * @description Comparison input, not necessarily measured
             */
            comparison_p_mp_w: number;
            /** Comparison V Mp V */
            comparison_v_mp_v: number;
            /** Comparison V Oc V */
            comparison_v_oc_v: number;
            /** Condition Id */
            condition_id: string;
            /**
             * Effective Irradiance W M2
             * @description Zero has undefined error table
             */
            effective_irradiance_w_m2: number;
        };
        /** LegacyIVCaseResult */
        LegacyIVCaseResult: {
            /** Condition Id */
            condition_id: string;
            /** Current A */
            current_a: number[];
            /** Desoto Inputs */
            desoto_inputs: {
                [key: string]: number;
            };
            /** Desoto Parameters */
            desoto_parameters: {
                [key: string]: number;
            };
            /** Singlediode */
            singlediode: {
                [key: string]: number;
            };
            /** Voltage V */
            voltage_v: number[];
        };
        /**
         * LegacyIVModule
         * @description Source coefficients retain percent/°C; the model owns interpretation.
         */
        LegacyIVModule: {
            /** Alpha Sc Percent Per C */
            alpha_sc_percent_per_c: number;
            /** Beta Voc Percent Per C */
            beta_voc_percent_per_c: number;
            /** Cells In Series */
            cells_in_series: number;
            /** Gamma Pmp Percent Per C */
            gamma_pmp_percent_per_c: number;
            /** I Mp A */
            i_mp_a: number;
            /** I Sc A */
            i_sc_a: number;
            /**
             * P Mp W
             * @description Retained source rating; unused by IV_R fit
             */
            p_mp_w: number;
            /** Source Cell Type */
            source_cell_type: string;
            /** Source Reference Temperature C */
            source_reference_temperature_c: number;
            /** V Mp V */
            v_mp_v: number;
            /** V Oc V */
            v_oc_v: number;
        };
        /** LegacyIVRequest */
        LegacyIVRequest: {
            /** Cases */
            cases: components["schemas"]["LegacyIVCase"][];
            /**
             * Model Id
             * @constant
             */
            model_id: "legacy-iv-r-v1";
            module: components["schemas"]["LegacyIVModule"];
            source_record?: components["schemas"]["SourceRecord"] | null;
        };
        /** LegacyIVResponse */
        LegacyIVResponse: {
            /** Cases */
            cases: components["schemas"]["LegacyIVCaseResult"][];
            /** Effective Assumptions */
            effective_assumptions: {
                [key: string]: string | number;
            };
            /** Fit Inputs */
            fit_inputs: {
                [key: string]: string | number;
            };
            /** Fit Parameters */
            fit_parameters: {
                [key: string]: number;
            };
            /**
             * Model Id
             * @default legacy-iv-r-v1
             * @constant
             */
            model_id: "legacy-iv-r-v1";
            /**
             * Reproduction Scope
             * @default Selected IV_R numerical boundary; full backend reproduction pending
             */
            reproduction_scope: string;
            /**
             * Scientific Status
             * @default Limited equation checks; an original Linux MPP audit target is unmet; no empirical validation
             */
            scientific_status: string;
            source_record: components["schemas"]["SourceRecord"] | null;
            /** Supplied Cases */
            supplied_cases: components["schemas"]["LegacyIVCase"][];
            supplied_module: components["schemas"]["LegacyIVModule"];
            /** Table Columns */
            table_columns: string[];
            /** Table Records */
            table_records: (string | number)[][];
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
    reproduceLegacyIV: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["LegacyIVRequest"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["LegacyIVResponse"];
                };
            };
            /** @description Bad Request */
            400: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["CalculationFailure"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
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

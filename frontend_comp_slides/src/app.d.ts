// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
	type User = {
		id: number
		username: string
	}

	namespace App {
		// interface Error {}
		interface Locals {
			user: User | null
		}
		// interface Locals {}
		// interface PageData {}
		// interface Platform {}
	}
}

export {};

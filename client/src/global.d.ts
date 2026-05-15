declare module "https://cdn.cubing.net/v0/js/cubing/scramble" {
	import type { Alg } from "cubing/alg";
	export function randomScrambleForEvent(event: string): Promise<Alg>;
}

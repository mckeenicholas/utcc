import type { Alg } from 'cubing/alg';
import type { WCAEvent } from './types';

interface ScrambleModule {
	randomScrambleForEvent: (eventID: WCAEvent) => Promise<Alg>;
}

let scrambleModule: ScrambleModule | null = null;

export const generateScrambles = async (eventId: WCAEvent, count: number): Promise<Alg[]> => {
	if (!scrambleModule) {
		// Importing the module from cubing.net's CDN is required as Rollup seems to be overly
		// aggressive in its minification, combining browser-only code into its worker chunks, causing
		// a document is undefined error.
		//
		// TODO: There may be a way to disable this in some advanced vite/rollup setting, however
		// this is a much lower priority since there is pretty much no downsides to this (as long as the cubing.net servers stay up).
		scrambleModule = await import('https://cdn.cubing.net/v0/js/cubing/scramble');
	}

	const { randomScrambleForEvent } = scrambleModule;

	return Promise.all(Array.from({ length: count }).map(() => randomScrambleForEvent(eventId)));
};

import type { Alg } from 'cubing/alg';
import type { WCAEvent } from './types';

interface ScrambleModule {
	randomScrambleForEvent: (eventID: WCAEvent) => Promise<Alg>;
}

let scrambleModule: ScrambleModule | null = null;

export const generateScrambles = async (eventId: WCAEvent, count: number): Promise<string[]> => {
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

	const scramblesAlgs = await Promise.all(
		Array.from({ length: count }).map(() => randomScrambleForEvent(eventId))
	);
	const scrambles = scramblesAlgs.map(String);

	if (eventId == '222') {
		return scrambles.map(normalize2x2Scramble);
	}

	return scrambles;
};

// The scramble generator generates 2x2 scrambles with L B D moves, which, while WCA compliant,
// Doesn't match what TNoodle generates.
// This function will 'correct' it by translating it to R U F only scrambles.
type Face = 'F' | 'B' | 'R' | 'U' | 'L' | 'D';
type Orientation = Record<Face, Face>;

const createRotator = (faces: [Face, Face, Face, Face]) => {
	const cw = (orientation: Orientation): void => {
		const temp = orientation[faces[0]];
		orientation[faces[0]] = orientation[faces[3]];
		orientation[faces[3]] = orientation[faces[2]];
		orientation[faces[2]] = orientation[faces[1]];
		orientation[faces[1]] = temp;
	};

	const ccw = (orientation: Orientation): void => {
		const temp = orientation[faces[0]];
		orientation[faces[0]] = orientation[faces[1]];
		orientation[faces[1]] = orientation[faces[2]];
		orientation[faces[2]] = orientation[faces[3]];
		orientation[faces[3]] = temp;
	};

	const half = (orientation: Orientation): void => {
		const temp1 = orientation[faces[0]];
		const temp2 = orientation[faces[1]];
		orientation[faces[0]] = orientation[faces[2]];
		orientation[faces[1]] = orientation[faces[3]];
		orientation[faces[2]] = temp1;
		orientation[faces[3]] = temp2;
	};

	return { cw, ccw, half };
};

const { cw: rotateX, ccw: rotateXCCW, half: rotateX2 } = createRotator(['F', 'U', 'B', 'D']);
const { cw: rotateY, ccw: rotateYCCW, half: rotateY2 } = createRotator(['F', 'L', 'B', 'R']);
const { cw: rotateZ, ccw: rotateZCCW, half: rotateZ2 } = createRotator(['U', 'R', 'D', 'L']);

const normalizedMoveActions = {
	R: { normal: rotateX, prime: rotateXCCW, half: rotateX2 },
	U: { normal: rotateY, prime: rotateYCCW, half: rotateY2 },
	F: { normal: rotateZ, prime: rotateZCCW, half: rotateZ2 }
};

const mirroredMoveActions = {
	L: { counterpart: 'R', normal: rotateXCCW, prime: rotateX, half: rotateX2 },
	D: { counterpart: 'U', normal: rotateYCCW, prime: rotateY, half: rotateY2 },
	B: { counterpart: 'F', normal: rotateZCCW, prime: rotateZ, half: rotateZ2 }
};

export const normalize2x2Scramble = (scramble: string): string => {
	if (!scramble) {
		return '';
	}

	const moves = scramble.split(/\s+/).filter(Boolean);

	// Initialize the cube's orientation
	const orientation: Orientation = {
		F: 'F',
		B: 'B',
		R: 'R',
		U: 'U',
		L: 'L',
		D: 'D'
	};

	const normalizedScramble: string[] = [];

	for (const move of moves) {
		const originalFace = move[0] as Face;
		const isTwo = move.length > 1 && move[1] === '2';
		const isPrime = move.length > 1 && move[1] === "'";

		let newMoveFace: Face | undefined;

		if (originalFace in mirroredMoveActions) {
			const action = mirroredMoveActions[originalFace as keyof typeof mirroredMoveActions];
			newMoveFace = action.counterpart as Face;
			if (isTwo) {
				action.half(orientation);
			} else if (isPrime) {
				action.prime(orientation);
			} else {
				action.normal(orientation);
			}
		} else if (originalFace in normalizedMoveActions) {
			const action = normalizedMoveActions[originalFace as keyof typeof normalizedMoveActions];
			newMoveFace = originalFace;
			if (isTwo) {
				action.half(orientation);
			} else if (isPrime) {
				action.prime(orientation);
			} else {
				action.normal(orientation);
			}
		}

		if (newMoveFace) {
			let newMove = newMoveFace;
			if (isTwo) {
				newMove += '2';
			} else if (isPrime) {
				newMove += "'";
			}
			normalizedScramble.push(newMove);
		}
	}

	return normalizedScramble.join(' ');
};

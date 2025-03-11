import type { WCAEvent } from './types';

export const Ao5 = (times: number[]): number => {
	if (times.length !== 5) {
		throw new Error('Ao5 requires exactly 5 times');
	}

	const sortedTimes = [...times].sort((a, b) => a - b);

	return Math.trunc((sortedTimes[1] + sortedTimes[2] + sortedTimes[3]) / 3) / 100;
};

export const Mo3 = (times: number[]): number => {
	if (times.length !== 3) {
		throw new Error('Mo3 requires exactly 3 times');
	}

	return Math.trunc((times[0] + times[1] + times[2]) / 3) / 100;
};

export const Bo3 = (times: number[]): number => {
	if (times.length !== 3) {
		throw new Error('Bo3 requires exactly 3 times');
	}

	return Math.min(...times) / 100;
};

export const calculateWCAAverage = (event: WCAEvent, times: number[]): number => {
	console.log(times);

	if (event === '666' || event === '777' || event === '333fm') {
		return Mo3(times);
	}

	if (event === '333bf' || event === '444bf' || event === '555bf') {
		return Bo3(times);
	}

	return Ao5(times);
};

export const compareTimes = (event: WCAEvent, times1: number[], times2: number[]): number => {
	const res = calculateWCAAverage(event, times1) - calculateWCAAverage(event, times2);
	if (res != 0) {
		return res;
	}

	return Math.min(...times1) - Math.min(...times2);
};

export const bestTime = (times: number[]): string => {
	const validTimes = times.filter((time) => time > 0);

	if (validTimes.length == 0) {
		return 'DNF';
	}

	const minTime = Math.min(...validTimes);

	return String(minTime / 100);
};

export const renderTime = (time: number): string => {
	if (time == -2) {
		return 'DNS';
	}

	if (time == -1) {
		return 'DNF';
	}

	if (time == 0) {
		return '';
	}

	return String(time / 100);
};

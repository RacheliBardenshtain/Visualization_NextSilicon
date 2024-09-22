#include "ILogFilter.h"

Generator<Log> ILogFilter::getNext() {
	while (base->isOpen())
		for (auto log : base->getNext())
			if (isToTake(log))
				co_yield log;
}

bool ILogFilter::isOpen() {
	return base->isOpen();
}
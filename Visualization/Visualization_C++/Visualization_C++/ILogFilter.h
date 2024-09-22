#pragma once
#include "LogReader.h"

class ILogFilter : public IView {

public:
	IViewPtr base;

	ILogFilter(IViewPtr toFilter) : base(toFilter) {}

	virtual bool isToTake(const Log& l) const = 0;

	Generator<Log> getNext() override;

	bool isOpen() override;

};
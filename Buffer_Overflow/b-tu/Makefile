# NOTE: This makefile disables all relevant protections already by default. You will need
# to re-enable them bit by bit during the course of this task sheet.
CXX      := g++
CXXFLAGS := -m32 -pedantic-errors -Wall -Wextra -Werror -U_FORTIFY_SOURCE -z execstack -fno-stack-protector -no-pie -Wl,-z,norelro
LDFLAGS  := -L/usr/lib32 -L./lib/Log -Wl,-rpath=./lib/Log/ -Wl,-z,norelro -lstdc++ -lm -lLog
BUILD    := ./build
OBJ_DIR  := $(BUILD)/objects
APP_DIR  := $(BUILD)/bin
TARGET   := btu
INCLUDE  := -Iinclude/
SRC      :=	$(wildcard src/University/*.cpp)	\
			$(wildcard src/*.cpp)

OBJECTS  := $(SRC:%.cpp=$(OBJ_DIR)/%.o)

all: build $(APP_DIR)/$(TARGET)

$(OBJ_DIR)/%.o: %.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $< -o $@ $(LDFLAGS)

$(APP_DIR)/$(TARGET): $(OBJECTS)
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) -o $(APP_DIR)/$(TARGET) $^ $(LDFLAGS)

.PHONY: all build clean debug release

build:
	@mkdir -p $(APP_DIR)
	@mkdir -p $(OBJ_DIR)

debug: CXXFLAGS += -DDEBUG -g
debug: all

release: CXXFLAGS += -O2
release: all

clean:
	-@rm -rvf $(OBJ_DIR)/*
	-@rm -rvf $(APP_DIR)/*
